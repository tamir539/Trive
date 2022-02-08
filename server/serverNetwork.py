import socket
import select
import queue
import threading
import time
import os
import sprotocol as prot
from Encryption import Defi

class ServerCom:

    def __init__(self, port, q, upload_server = False, download_server = False, edit_server = False):
        '''

        :param port:port to talk with a client
        :param q:
        '''
        self.servSoc = None
        self.port = port
        self.q = q
        self.socs = {}  #socket -> his ip adress
        self.running = True
        self.upload_server = upload_server  #true - > need to recv file
        self.download_server = download_server      #"true" -> need to send file
        self.edit_server = edit_server      #true - need to recive file with no answer to the client
        self.has_client = False     #true -> client connected, false otherwise
        threading.Thread(target=self.recv_msg).start()

    def send_msg(self, ip, msg):
        '''

        :param soc:client socket
        :param msg: string
        :return: sends the string to the socket
        '''
        if type(msg) == 'str':
            msg = msg.encode()
        soc = self.get_soc_by_ip(ip)
        if soc:
            try:
                soc.send(str(len(msg)).zfill(3).encode())
                soc.send(msg)
            except Exception as e:
                print(f'in sendMsg - {str(e)}')

    def send_file(self, path, client_key, server_key):
        '''

        :param client_key: aes of the client to decrypt the file after sending
        :param server_key: aes of the server files to encrypt the file
        :param path:path to the file
        :param soc: client socket
        :return: send the file to the client
        '''
        while not self.has_client:
            pass
        time.sleep(0.2)
        file = open(path, 'rb')
        data = file.read()
        file.close()
        try:
            list(self.socs.keys())[0].send(data)
            self.running = False
            self.servSoc.close()
        except Exception as e:
            print(f'in send file - {str(e)}')
        else:
            client_key.decrypt_file(path)
            server_key.encrypt_file(path)

    def recv_msg(self):

        self.servSoc = socket.socket()
        self.servSoc.bind(('0.0.0.0',self.port))
        self.servSoc.listen(3)

        while self.running:
            rlist, wlist, xlist = select.select(list(self.socs.keys())+[self.servSoc],list(self.socs.keys()),[],0.3)
            for current_socket in rlist:
                if current_socket is self.servSoc:
                    # new client
                    client, address = self.servSoc.accept()
                    if not self.check_if_blocked(address[0]) and not self.upload_server and not self.download_server:
                        print(f'{address[0]} - connected')
                        threading.Thread(target= self.switch_keys, args= (client, address[0], )).start()
                    elif not self.check_if_blocked(address[0]) and (self.upload_server or self.download_server):
                        #if download or upload server, no switch keys
                        self.has_client = True
                        self.socs[client] = address[0]
                    else:
                        self.send_msg(client, 'blocked')
                else:
                    # receive data from exist client
                    try:
                        msg_len = current_socket.recv(3).decode()
                        msg = current_socket.recv(int(msg_len))
                    except Exception as e:
                        print('in recv - ',self.port,  str(e))
                        del self.socs[current_socket]
                    else:
                        if not self.upload_server:
                            #recive regular msg
                            self.q.put((msg, self.socs[current_socket]))
                        else:
                            #recive upload msg
                            command, args = prot.unpack_msg(msg)
                            length, file_path, file_name  = args
                            self.recv_file(length, file_path, file_name)

    def switch_keys(self, soc, ip):
        '''

        :param soc:client socket
        :param ip: ip of the client
        :return: switch keys with the client
        '''
        defi = Defi()
        msg = str(defi.publish())
        try:
            soc.send(msg.encode())
            recived = int(soc.recv(5).decode())
        except Exception as e:
            print(f'in switch_keys 1 - {str(e)}')
        else:
            key = str(defi.compute_secret(recived))
            self.q.put(('key', key, ip))
            #add the socket to the socket that switched keys
            self.socs[soc] = ip

    def recv_file(self, file_len, file_path, file_name):
        '''

        :param file_len:length of the file to recive
        :param file_name: name of the file
        :return: recive all the file data, save it in the uploads folder, notify with msg in q when finish
        '''
        file_data = bytearray()
        file_len = int(file_len)
        # recv all the data
        while len(file_data) < file_len:
            size = file_len - len(file_data)
            try:
                if size >= 1024:
                    file_data.extend(list(self.socs.keys())[0].recv(1024))
                else:
                    if size != 0:
                        file_data.extend(list(self.socs.keys())[0].recv(size))
                    break
            except Exception as e:
                print(f'in recv file - {str(e)}')
                file_data = None
                break

        if file_data is not None:
            with open(file_path + '\\' + file_name, 'wb') as f:
                f.write(file_data)
                f.close()
            if self.edit_server:
                self.q.put(('upload', 'ok', True, file_path, file_name, self.socs[list(self.socs.keys())[0]]))
            else:
                self.q.put(('upload', 'ok', False, file_path, file_name, self.socs[list(self.socs.keys())[0]]))
        else:
            if self.edit_server:
                self.q.put(('upload', 'no', True, file_path, file_name, self.socs[list(self.socs.keys())[0]]))
            else:
                self.q.put(('upload', 'no', False, file_path, file_name, self.socs[list(self.socs.keys())[0]]))
        self.servSoc.close()
        self.socs = {}
        self.running = False

    def check_if_blocked(self, ip):
        '''

        :param ip:ip
        :return: "true" - if this ip is blocked and "false" otherwise
        '''
        ips = open('blocked_ips.txt', 'r').read().split('\n')
        return ip in ips

    def block_ip(self, ip):
        '''

        :param ip:ip
        :return: add the ip to the file of block ips
        '''
        ip = str(ip)
        block_ip_file = open('blocked_ips.txt', 'a')
        block_ip_file.write(ip + '\n')
        block_ip_file.close()

    def get_soc_by_ip(self, ip):
        '''

        :param ip:ip of user
        :return: the socket of this ip
        '''

        for soc in self.socs.keys():
            if self.socs[soc] == ip:
                return soc
        return None