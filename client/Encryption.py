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
        '''

        :param message:massage to encrypt
        :return: encrypted massage
        '''
        if type(message) is str:
            message = message.encode()
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(message))

    def decrypt(self, ciphertext, file = False):
        '''

        :param ciphertext:msg to decrypt
        :param file: "true" - decrypt file, "false" - decrypt string
        :return: decrypted massage
        '''
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        if file:
            return plaintext.rstrip(b"\0")
        else:
            return plaintext.rstrip(b"\0").decode()

    def encrypt_file(self, file_path, new_path):
        '''

        :param file_name:file path to encrypt
        :return: the new path to the encrypted file
        '''
        file_name = file_path[file_path.rindex('\\'):]
        with open(file_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(new_path + file_name, 'wb') as fo:
            fo.write(enc)
        return new_path + file_name

    def decrypt_file(self, file_path):
        '''

        :param file_path: path of the file to decrypt
        :return:decrypt the file
        '''
        with open(file_path, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext).encode()
        with open(file_path, 'wb') as fo:
            fo.write(dec)


class Defi:
    def __init__(self):
        self.a = random.randint(1, 100000)

    def publish(self):
        return 47 ** self.a % 100000

    def compute_secret(self, gb):
        return gb ** self.a % 100000

