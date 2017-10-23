#!/usr/bin/python
import sys, getopt, logging
sys.path.append("/root/scripts")
from  aac_toolbox.toolbox.GlobalVariable import *
import paramiko
import getpass
from ContentManager import ContentManager

IPADDRESS = ''
EDBHOME = ''
logging.debug("loglevel: "+str(GlobalVariable.loglevel))

def printf(format, *args):
    sys.stdout.write(format % args)

def usage():
        printf ("create_bartpem.py -i <ip> -s <hostname> -u <use> -v <DB version> -h \n")
        printf ("-i ip address\n")
        printf ("-s lowercase servername\n")
        printf ("-u Use = UAT or PROD\n")
        printf ("-v DB version = 94 or 96\n")
        printf ("-h HELP =  display this message\n")

def get_sshstr(outputlist):
        sshkey = ''.join(outputlist)
        return sshkey


def get_sshkey():
    	global IPADDRESS
    	global EDBHOME
	logging.debug(EDBHOME)
	username = GlobalVariable.username
	password = GlobalVariable.password
        command = 'sudo cat '+EDBHOME+'/.ssh/id_rsa.pub'
        port = 22

        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(IPADDRESS, port, username, password)
        stdin, stdout, stderr = s.exec_command(command, get_pty = True)
        stdin.write(password + "\n")
        stdin.flush()
        output = stdout.readlines()
	sshkey = get_sshstr(output)
	logging.info("username: "+username+" password: "+ password)
	return sshkey

def gethostname(hostname):
	locate = hostname.find(".")
	if locate == -1:
	  return hostname
        else:
          HOSTNAME = hostname[0:locate-1]
	return HOSTNAME
		

def main (): 
    global IPADDRESS
    global EDBHOME
    try:
      if len(sys.argv) <= 1:
          usage()
          sys.exit(2)
      opts, args = getopt.getopt(sys.argv[1:], "i:s:u:v:h")
    except getopt.GetoptError:
      usage()
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-v':
        DBVER = arg 
        if DBVER == '94':
           EDBHOME = '/var/lib/ppas'
	else:
           EDBHOME = '/var/lib/edb'
      elif opt == '-i':
        IPADDRESS = arg
        logging.debug(IPADDRESS)
      elif opt == '-s':
        HOSTNAME = gethostname(arg)
      elif opt == '-u':
        USEAGE = arg
      elif opt == '-h':
        usage()
        sys.exit()
     	
    SSHKEY = get_sshkey()
    logging.debug("sshkey: "+SSHKEY+" HOSTNAME: "+HOSTNAME)
    contents = ContentManager(IPADDRESS,HOSTNAME,USEAGE,DBVER,SSHKEY)
    contents.GetUpdatedContent()
    contents.Update_Content()
    
if __name__ == '__main__':
    main()

