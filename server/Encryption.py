from Crypto.Cipher import AES
from Crypto import Random
import random
#finish comments!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class AESCipher(object):
    def __init__(self, key):
        '''

        :param key:string to create the aes key with
        '''
        self.key = key + (32 - len(key)) * ' '
        self.key = self.key.encode()

    def pad(self, s):
        '''

        :param s:string to pad
        :return: pad the string to be ajusted to the encrypt
        '''
        padding_size = AES.block_size - len(s) % AES.block_size
        return s + b"\0" * padding_size, padding_size

    def encrypt(self, message):
        '''

        :param message:massage to encrypt
        :return: encrypted massage
        '''
        if type(message) is str:
            message = message.encode()
        message, padding_size = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message) + bytes([padding_size])

    def decrypt(self, ciphertext, file=False):
        '''

        :param ciphertext:msg to decrypt
        :param file: "true" - decrypt file, "false" - decrypt string
        :return: decrypted massage
        '''
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:-1])
        padding_size = ciphertext[-1] * (-1)
        if file:
            return plaintext[:padding_size]
        else:
            return plaintext.rstrip(b"\0").decode()

    def encrypt_file(self, file_path):
        '''

        :param file_path: file path to encrypt
        :return: the new path to the encrypted file
        '''
        with open(file_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_path, 'wb') as fo:
            fo.write(enc)

    def decrypt_file(self, file_path):
        '''

        :param file_path: path of the file to decrypt
        :return:decrypt the file
        '''
        with open(file_path, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, True)
        with open(file_path, 'wb') as fo:
            fo.write(dec)


class Defi:
    def __init__(self):
        self.a = random.randint(1, 100000)

    def publish(self):
        '''

        :return:compute own number to send to the server
        '''
        return 47 ** self.a % 100000

    def compute_secret(self, gb):
        '''

        :param gb:int recived from the server
        :return: copute the recived integer with self integer and return the common integer
        '''
        return gb ** self.a % 100000



if __name__ == '__main__':
    key = 'tamir'

    my_key = AESCipher(key)

    #my_key.encrypt_file('c:\\temp\\aaa.py.txt')
    my_key.decrypt_file('c:\\temp\\aaa.py.txt')

