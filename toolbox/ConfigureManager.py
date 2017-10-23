#!/usr/bin/python
import sys, logging, json
from PasswordManager import *

class ConfigureManager:

	def __init__(self, configfile):
	  self.configfile = configfile
	  self.config = json.loads(open(configfile).read())

        def getloglevel(self):
	  loglevel = self.config["loglevel"]  
	  return loglevel	  
 
	def getusername(self):
	  username = self.config["username"]
	  logging.debug("username: "+username)
	  return username

	def getpassword(self):
	  encryptpass = str(self.config["enpassword"])
	  key = self.config["key"]
	  logging.info("encrypt password: "+encryptpass)	
	  passwordmanager = PasswordManager(key)
	  decryptpass = passwordmanager.decryptpassword(encryptpass)
	  logging.debug("password: "+decryptpass)
	  return decryptpass
	
	    
