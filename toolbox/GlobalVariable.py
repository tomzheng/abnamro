import sys,logging
from ConfigureManager import *

class GlobalVariable:
  configmanager = ConfigureManager("../cfg/aac_toolbox.cfg")
  log_level = configmanager.getloglevel()
  loglevel = getattr(logging, log_level.upper(), 10)
  logging.basicConfig(stream=sys.stderr, level=loglevel)
  logging.info("loglevel: "+log_level+" "+str(loglevel))
  username = configmanager.getusername()
  password = configmanager.getpassword()
  logging.debug("username: "+username)
  logging.debug("password: "+password)


