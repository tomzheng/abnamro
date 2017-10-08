import sys,logging
sys.path.append("/root/scripts")
from aac_toolbox.toolbox.TemplateManager import *

cookbookpath = "/root/chef-repo/cookbooks/haproxy"
class ContentManager:
  logging.basicConfig(stream=sys.stderr, level=logging.INFO)
  def __init__(self,app,usage,client,keyserial,hostname,port):
    self.app = app
    self.usage = usage
    self.client = client
    self.keyserial = keyserial
    self.hostname = hostname
    self.port = port
    self.haproxy_cfg_frontend = ""
    self.haproxy_cfg_backend = ""


  def GetUpdatedContent(self):
    self.Get_haproxy_frontend()
    self.Get_haproxy_backend()

  def Get_haproxy_frontend(self):
    self.haproxy_cfg_frontend = """
    acl cert_%s%s_%s ssl_c_serial -m bin %s
    use_backend %s%s_%s if cert_%s%s_%s

""" %(self.app,self.usage,self.client,self.keyserial,self.app,self.usage,self.client,self.app,self.usage,self.client)
 	
  def Get_haproxy_backend(self):
    self.haproxy_cfg_backend = """

#---------------------------------------------------------------------
# %s%s_%s
#---------------------------------------------------------------------

backend %s%s_%s
    mode tcp
    balance     roundrobin
    server  %s%s_%s localhost:%s

""" %(self.app, self.usage, self.client,self.app, self.usage,self.client, self.app, self.usage,self.client, self.port)


  def Update_Content(self):
    templatemanager = TemplateManager()
    templatefilepath = "/templates/haproxy.cfg."+self.hostname+".erb"
    ignorekey_frontend = 'cert_'+self.app+self.usage+'_'+self.client
    ignorekey_backend = 'server  '+self.app+self.usage+'_'+self.client
    templatemanager.insert_file_if_notfound(cookbookpath + templatefilepath,ignorekey_frontend ,self.haproxy_cfg_frontend,"#frontend setting, edited by haproxy script on sgvlapaacchefs")
    templatemanager.append_file_if_notfound(cookbookpath + templatefilepath,ignorekey_backend, self.haproxy_cfg_backend)

		
		
		
		
