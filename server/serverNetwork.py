import socket
import select
import queue
import threading
import time
import os

class ServerCom:

    def __init__(self, port, q):
        '''

        :param port:port to talk with a client
        :param q:
        '''
        self.servSoc = None
        self.port = port
        self.q = q
        self.socs = {}  #socket -> his ip adress
        self.running = True
        threading.Thread(target=self.recv_msg).start()

    def send_msg(self, soc, msg):
        '''

        :param soc:client socket
        :param msg: string
        :return: sends the string to the socket
        '''
        if soc in self.socs.keys():
            try:
                soc.send(str(len(msg)).encode())
                soc.send(msg.encode())
            except Exception as e:
                print(f'in sendMsg - {str(e)}')

    def send_file(self, path):
        '''

        :param path:path to the file
        :param soc: client socket
        :return: send the file to the client
        '''
        time.sleep(0.2)
        file = open(path, 'rb')
        data = file.read()
        try:
            list(self.socs.keys())[0].send(data)
            self.running = False
            self.servSoc.close()
        except Exception as e:
            print(f'in send file - {str(e)}')

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
                    if not self.check_if_blocked(address[0]):
                        print(f'{address[0]} - connected')
                        self.socs[client] = address[0]
                    else:
                        self.send_msg(client, 'blocked')
                        print('sent block')
                else:
                    # receive data from exist client
                    try:
                        msg_len = current_socket.recv(2).decode()
                        msg = current_socket.recv(int(msg_len)).decode()
                    except Exception as e:
                        print('in recv - ', str(e))
                        del self.socs[current_socket]
                    else:
                        self.q.put((msg, current_socket, self.socs[current_socket]))

    def recv_file(self, file_len, file_name):
        '''

        :param file_len:length of the file to recive
        :param file_name: name of the file
        :return: recive all the file data, save it in the uploads folder, notify with msg in q when finish
        '''
        print('22222')
        file_data = bytearray()
        # recv all the data
        while len(file_data) < file_len:
            print(1)
            size = file_len - len(file_data)
            try:
                if size >= 1024:
                    file_data.extend(self.socs[0].recv(1024))
                else:
                    file_data.extend(self.socs[0].recv(size))
                    break
            except Exception as e:
                print(f'in recv file - {str(e)}')
                file_data = None
                break

        if file_data is not None:
            path = 'C:\\Trive\\uploads'
            try:
                os.makedirs(path)
            except Exception as e:
                print(f'in recv file 2 - {str(e)}')
            else:
                with open(path+'\\'+file_name, 'wb') as f:
                    f.write(file_data)
                self.q.put((f'got-{file_name}', self.socs[0]))
                print(self.q.get())

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
