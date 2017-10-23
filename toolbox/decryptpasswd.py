#!/usr/bin/python
import sys, logging
from PasswordManager import *


def decryptpass(passwd, key):
    passwordmanager = PasswordManager(key)
    decryptpass = passwordmanager.decryptpassword(passwd)
    return decryptpass

def main ():
    key = raw_input("Please input decrypt key:\n")
    password = raw_input("Please input decrypted password:\n")   
    decrypt_pass = decryptpass(password, key) 
    logging.info("Decrypt password: "+decrypt_pass)

if __name__ == '__main__':
    main()





