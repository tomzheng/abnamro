import sys,logging,base64

class PasswordManager:
  def __init__(self,key):
    self.key = key

  def encryptpassword(self,clear):
    enc = []
    for i in range(len(clear)):
        key_c = self.key[i % len(self.key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))

  def decryptpassword(self,enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = self.key[i % len(self.key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
