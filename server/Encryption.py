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

    def decrypt(self, ciphertext):
        '''

        :param ciphertext:msg to decrypt
        :return: decrypted massage
        '''
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0").decode()

    def encrypt_file(self, file_path):
        '''

        :param file_name:file path to encrypt
        :return: the new path to the encrypted file
        '''
        file_name = file_path[file_path.rindex('\\'):]
        with open(file_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_path, 'wb') as fo:
            fo.write(enc)

    def decrypt_file(self, file_path):
        print(file_path)
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



if __name__ == '__main__':
    key = 'tamir'

    my_key = AESCipher(key)

    text = my_key.encrypt('tamir')
    print(text)
    print(my_key.decrypt(text))

    #my_key.encrypt_file('c:\\temp\\new_cat.png')
    #my_key.decrypt_file('c:\\temp\\temp.png.enc')

