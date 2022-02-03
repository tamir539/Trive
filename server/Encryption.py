import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import random


class AESCipher(object):
    # def __init__(self, key):
    #     self.bs = AES.block_size
    #     self.key = hashlib.sha256(key.encode()).digest()
    #
    # def encrypt(self, raw):
    #     '''
    #
    #     :param raw: msg to encrypt
    #     :return: the msg encrypted
    #     '''
    #     if type(raw) == 'str':
    #         raw = raw.encode()
    #     raw = self._pad(raw)
    #     iv = Random.new().read(AES.block_size)
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return base64.b64encode(iv + cipher.encrypt(raw))
    #
    # def decrypt(self, enc):
    #     '''
    #
    #     :param enc:encrypted msg
    #     :return: the decrypted msg
    #     '''
    #     enc = base64.b64decode(enc)
    #     iv = enc[:AES.block_size]
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
    #
    # def _pad(self, s):
    #     #return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    #     return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    #
    # @staticmethod
    # def _unpad(s):
    #     return s[:-ord(s[len(s)-1:])]
    #
    #
    # def encrypt_file(self, path):
    #
    #     with open(path, 'rb') as read_file:
    #         data = read_file.read()
    #     enc_data = self.encrypt(data)
    #     with open(path + '.enc', 'wb') as out_file:
    #         out_file.write(enc_data)
    #     return path + '.enc'
    #
    # def decrypt_file(self, file_name):
    #     with open(file_name, 'rb') as fo:
    #         ciphertext = fo.read()
    #
    #     print(type(ciphertext))
    #     dec = self.decrypt(ciphertext)
    #     dec = dec.encode()
    #     print(type(dec))
    #     with open(file_name[:-4], 'wb') as fo:
    #         fo.write(dec)

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

    def encrypt_file(self, file_name ):
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



if __name__ == '__main__':
    key = 'tamir'

    my_key = AESCipher(key)

    text = my_key.encrypt('tamir')
    print(text)
    print(my_key.decrypt(text))

    #my_key.encrypt_file('c:\\temp\\new_cat.png')
    #my_key.decrypt_file('c:\\temp\\temp.png.enc')

