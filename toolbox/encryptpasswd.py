#!/usr/bin/python
import sys, logging
from PasswordManager import *


def encryptpass(passwd, key):
    passwordmanager = PasswordManager(key)
    encryptpass = passwordmanager.encryptpassword(passwd)
    return encryptpass

def main ():
    key = raw_input("Please input encrypt key:\n")
    password = raw_input("Please input password:\n")   
    encrypt_pass = encryptpass(password, key) 
    logging.info("Encrypt password: "+encrypt_pass)

if __name__ == '__main__':
    main()





