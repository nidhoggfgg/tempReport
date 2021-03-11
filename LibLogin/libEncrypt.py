from urllib import parse
import math
import random
import base64
from Crypto.Cipher import AES


class Encrypt:
    def __init__(self, data, salt, iv='6' * 16, chars="ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678", randomStringLen=64, charset="utf-8"):
        self.charset   = charset
        self.salt      = salt.encode(self.charset)
        self.iv        = iv.encode(self.charset)
        self.blockSize = 16
        self.dataLen   = len(data)
        self.chars     = chars
        self.data = self.randomString(randomStringLen) + data + \
            (self.blockSize - self.dataLen % self.blockSize)  * \
            chr(self.blockSize - self.dataLen % self.blockSize)


    def randomString(self, length):
        rdString = ""
        for i in range(0, length):
            charIndex = math.floor(random.random() * len(self.chars))
            rdString += self.chars[charIndex]
        return rdString


    def parseUrl(self, s):
        return parse.quote(s)


    def AES(self):
        cipher = AES.new(self.salt, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(bytes(self.data, encoding=self.charset))
        return str(base64.b64encode(encrypted), self.charset)


    def encrypt(self):
        return self.parseUrl(self.AES())
