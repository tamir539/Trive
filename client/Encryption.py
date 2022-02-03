import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import random


class AESCipher(object):
    def __init__(self, key):
        self.key = key + (32 - len(key)) * ' '
        self.key = self.key.encode()

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message):
        if type(message) is str:
            message = message.encode()
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(message))

    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0").decode()

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)


    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext).encode()
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)


class Defi:
    def __init__(self):
        self.a = random.randint(1, 100000)

    def publish(self):
        return 47 ** self.a % 100000

    def compute_secret(self, gb):
        return gb ** self.a % 100000
