import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import random


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        '''

        :param raw: msg to encrypt
        :return: the msg encrypted
        '''
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        '''

        :param enc:encrypted msg
        :return: the decrypted msg
        '''
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class Defi:
    def __init__(self):
        self.a = random.randint(1, 283)

    def publish(self):
        return 47 ** self.a % 283

    def compute_secret(self, gb):
        return gb ** self.a % 283