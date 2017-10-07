#!/usr/bin/python
import sys, getopt, logging
import paramiko
import getpass
from ContentManager import ContentManager
KEYHOST = ''
KEYDIRECTORY = ''
APP = ''

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def printf(format, *args):
    sys.stdout.write(format % args)

def usage():
        printf ("create_haproxy_user.py -s <servername> -c <client> -p <port> -u <use> -h \n")
        printf ("-s Server name\n")
        printf ("-c Client name\n")
        printf ("-p port number\n")
        printf ("-u Use = uat, prd or con\n")
	
def get_keyfilefromhostname(hostname, use, client):
	global APP
	if 'etf' in hostname:
   	  app = 'etf'
	elif 'rdc' in hostname:
	  app = 'rdc'
	keyserialfile = app+'_'+use+'_'+client+'.serial'
	APP = app
	return keyserialfile
		

def get_keyserial(keyfile):
        global KEYDIRECTORY
	global KEYHOST
	KEYHOST = 'SGVLAPAACintran.bcc.ap.abn'
	KEYDIRECTORY = "/fcs/extranet_admin/certs/"
        logging.debug(KEYDIRECTORY)
        port = 22
        username = raw_input("Please input username:")
        password = getpass.getpass('Please input password:')
        command = "sudo -u root sh -c 'cat "+KEYDIRECTORY+keyfile+"'"
        logging.debug('COMMAND: '+command)
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(KEYHOST, port, username, password)
        stdin, stdout, stderr = s.exec_command(command, get_pty = True)
	stdin.write(password + "\n")
	stdin.flush()
        keyserial = stdout.readlines()
        logging.debug('keyserial: '+''.join(keyserial))
        s.close()
        return keyserial


def main ():
    global KEYDIRECTORY
    global APP
    try:
      if len(sys.argv) <= 1:
          usage()
          sys.exit(2)
      opts, args = getopt.getopt(sys.argv[1:], "s:c:p:u:h")
    except getopt.GetoptError:
      usage()
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-c':
        CLIENT = arg.lower()
      elif opt == '-s':
        HOSTNAME = arg.lower()
      elif opt == '-p':
        PORT = arg
      elif opt == '-u':
        USE = arg.lower()
      elif opt == '-h':
        usage()
        sys.exit()
		
    keyfile = get_keyfilefromhostname(HOSTNAME, USE,CLIENT)
    logging.debug(keyfile)
    KEYSERIAL = get_keyserial(keyfile)
    logging.debug("KEYSERIAL: "+''.join(KEYSERIAL))
    contents = ContentManager(APP,USE, CLIENT,KEYSERIAL,HOSTNAME,PORT)
    contents.GetUpdatedContent()
    contents.Update_Content()

if __name__ == '__main__':
    main()

