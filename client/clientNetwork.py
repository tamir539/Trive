import socket
import queue
import threading
import os
import time
import cprotocol as prot
from Encryption import Defi


class ClientCom:

    def __init__(self, serverIp, serverPort, q, file = False, key = None):
        '''

        :param file: "true" if this network is to recv file and "false" otherwise
        :param serverIp:ip of the server
        :param serverPort: port to talk with the server
        :param q: queue that for trnsger data between the network to the main client
        '''
        self.file = file
        self.serverIp = serverIp
        self.serverPort = serverPort
        self.q = q
        self.soc = socket.socket()
        if not file and not key:
            threading.Thread(target = self.switch_keys, daemon=True).start()
        elif file:

            self.connect()
        else:
            self.key = key
            self.connect()
            threading.Thread(target=self.recv_file, daemon=True).start()

    def switch_keys(self):
        '''

        :return:switch keys with the server
        '''

        defi = Defi()
        my_publish = defi.publish()
        try:
            self.soc.connect((self.serverIp, self.serverPort))
            server_publish = int(self.soc.recv(5).decode())
            self.soc.send(str(my_publish).encode())
        except Exception as e:
            print(f'in recv msg - {str(e)}')
        else:
            key_str = str(defi.compute_secret(server_publish))
            self.q.put(f'key-{key_str}')
            threading.Thread(target=self.__recv_msg__(), daemon=True).start()

    def connect(self):
        try:
            self.soc.connect((self.serverIp, self.serverPort))
        except Exception as e:
            print(f'in connect - {str(e)}')

    def __recv_msg__(self):
        '''

        :return:recive msg from the server and put the msg in q
        '''
        while True:
            try:
                msg_len = int(self.soc.recv(3).decode())
                msg = self.soc.recv(msg_len)
            except Exception as e:
                print(f'in recv msg 2 - {str(e)}')
                self.soc.close()
                exit()
            else:
                self.q.put(msg)

    def send_msg(self, msg):
        '''

        :param msg: string
        :return: sends the msg to the server
        '''
        if type(msg) == 'str':
            msg = msg.encode()
        try:
            self.soc.send(str(len(msg)).zfill(3).encode())
            self.soc.send(msg)
        except Exception as e:
            print(f'in send msg - {str(e)}')
            self.soc.close()

    def send_file(self, filePath, server_path, file_name, key):
        '''

        :param filePath: path for file
        :return: sends the data to the server
        '''
        time.sleep(0.1)
        file = open(filePath, 'rb')
        data = file.read()
        msg_after_protocol = prot.create_upload_file_msg(server_path, len(data), file_name)
        total_msg = str(len(msg_after_protocol)).zfill(3) + msg_after_protocol
        #035051336&D:\Trive\tamir&Encryption.py
        try:
            self.soc.send(total_msg.encode())
            self.soc.send(data)
        except Exception as e:
            print(f'in send file - {str(e)}')
            self.soc.close()

    def recv_file(self, fileLen, fileName):
        '''

        :return:recv file from the server, download the file to downloads and add msg to q when finish recive
        '''
        file_data = bytearray()
        fileLen = int(fileLen)
        #recv all the data
        while len(file_data) < fileLen:
            size = fileLen - len(file_data)
            try:
                if size >= 1024:
                    file_data.extend(self.soc.recv(1024))
                else:
                    file_data.extend(self.soc.recv(size))
                    break
            except Exception as e:
                print(f'in recv file - {str(e)}')
                self.q.put('no')
                self.soc.close()
                file_data = None
                break

        if file_data is not None:
            path = os.path.expanduser('~/Downloads')
            with open(f'{path}\\{fileName}', 'wb') as f:
                f.write(file_data)
                self.q.put('ok')

        self.soc.close()

