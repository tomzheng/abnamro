import sys,logging

#cookbookpath = "/root/chef-repo/cookbooks/bartpem"
cookbookpath = "/home/BCC/admzheng/bartpem"
class ContentManager:

	def __init__(self, ipaddress, hostname, usage, dbversion, sshkey):
		self.ipaddress = ipaddress
		self.hostname = hostname
		self.usage = usage
		self.dbversion = dbversion
		self.sshkey = sshkey
		self.bart_cfg_content = ""
		self.pg_hba_content = ""
                self.usage_hostname = usage+"-"+hostname


	def GetUpdatedContent(self):
		self.Get_pg_hba_content()
		self.Get_bartcfg_content()
		self.Get_BART_BACKUP_content()
		self.Get_pgpass_content()

	def Get_pg_hba_content(self):
		self.pg_hba_content = """
 hostssl pem +pem_user %s/32 md5
 hostssl pem +pem_agent %s/32 cert""" %(self.ipaddress, self.ipaddress)
 	
	def Get_bartcfg_content(self):
		self.bart_cfg_content = """
[%s-%s]
host = %s.bcc.ap.abn
port = 5444
user = bartbackup
backup-name = %s-%s_%%year%%month%%dayT_%%hour%%minute%%second
remote-host = enterprisedb@%s.bcc.ap.abn
retention_policy = 7 DAYS
description = "PPAS%s-%s-%s""""" %(self.usage, self.hostname, self.hostname, self.usage, self.hostname,self.hostname, self.dbversion, self.usage,self.hostname)

	def Get_BART_BACKUP_content(self):
		if self.dbversion == '94':
			bartcfg = "bart.cfg"
		else:
			bartcfg = "bart_edb-as96.cfg"
		self.BART_BACKUP_content = """
#[%s-%s]
/usr/edb-bart-1.1/bin/bart -c /usr/edb-bart-1.1/etc/%s --debug backup -s %s-%s -z
if [ ! $? -ne 0 ]
then
	echo "BART backup completed successfully for server '%s-%s'"
else
	echo "BART backup failed for server '%s-%s'"
	echo "Backup failed for server '%s-%s'"|mailx -v -s "BART Backup Status on `date`" apacinfrastructure@au.abnamroclearing.com
fi""" %(self.usage, self.hostname,bartcfg, self.usage, self.hostname, self.usage, self.hostname,self.usage, self.hostname, self.usage, self.hostname)

	def Get_pgpass_content(self):
		self.pgpass_content = """%s.bcc.ap.abn:5444:*:bartbackup:bartbackup
""" %(self.hostname)

	def Update_Content(self):
		self.insert_file_if_notfound(cookbookpath + "/templates/pg_hba.conf.erb",self.ipaddress,self.pg_hba_content," # Allow remote PEM agents and users to connect to PEM server")
		if self.dbversion == '94':
			self.append_file_if_notfound(cookbookpath + "/templates/bart.cfg.erb",self.usage_hostname, self.bart_cfg_content)
		else:
			self.append_file_if_notfound(cookbookpath + "/templates/bart_edb-as96.cfg.erb",self.usage_hostname, self.bart_cfg_content)
		self.append_file_if_notfound(cookbookpath + "/templates/authorized_keys2.erb",self.sshkey, self.sshkey)
		self.append_file_if_notfound(cookbookpath + "/templates/" + self.usage + "_BART_BACKUP.sh.erb",self.usage_hostname,self.BART_BACKUP_content)
		self.append_file_if_notfound(cookbookpath + "/templates/pgpass.erb", self.hostname+"bcc.apa.abn", self.pgpass_content)

	def append_file_if_notfound(self, filename,ignorekey,content):
		with open (filename, "r+") as f:
			for line in f:
				if ignorekey in line:
					break
			else:
				f.write(content)

	def insert_file_if_notfound(self, filename,ignorekey,content,matchkey):
		logging.debug("pg_hba:"+content)
		inputfile = open(filename, 'r').readlines()
		found = False
		for line in inputfile:
			if ignorekey in line:
			        found = True		
				break
		
                if not found:
			writefile = open(filename,'w')
			for line in inputfile:
				writefile.write(line)
				if matchkey in line:
					writefile.write(content)
			writefile.close()
		
		
		
		
