import socket
import select
import queue
import threading

class ServerCom:

    def __init__(self, port, q):
        '''

        :param port:port to talk with a client
        :param q:
        '''
        self.servSoc = None
        self.port = port
        self.q = q
        self.socs = []
        threading.Thread(target=self.recv_msg).start()

    def send_msg(self, soc, msg):
        '''

        :param soc:client socket
        :param msg: string
        :return: sends the string to the socket
        '''
        if soc in self.socs:
            try:
                soc.send(str(len(msg)).encode())
                soc.send(msg.encode())
            except Exception as e:
                print(f'in sendMsg - {str(e)}')

    def send_file(self, path, soc):
        '''

        :param path:path to the file
        :param soc: client socket
        :return: send the file to the client
        '''
        file = open(path, 'rb')
        data = file.read()
        try:
            soc.send(data)
        except Exception as e:
            print(f'in send file - {str(e)}')

    def recv_msg(self):
        self.servSoc = socket.socket()
        self.servSoc.bind(('0.0.0.0',self.port))
        self.servSoc.listen(3)

        while True:
            rlist, wlist, xlist = select.select(self.socs + [self.servSoc], self.socs, [],0.3)
            for current_socket in rlist:
                if current_socket is self.servSoc:
                    # new client
                    client, address = self.servSoc.accept()
                    print(f'{address[1]} - connected')
                    self.socs.append(client)
                else:
                    # receive data from exist client
                    try:
                        msg_len = current_socket.recv(2).decode()
                        print('len - ', msg_len)
                        msg = current_socket.recv(int(msg_len)).decode()
                        print('msg - ',msg)
                        self.send_file(msg, current_socket)
                    except Exception as e:
                        print('in recv - ', str(e))
                        self.socs.remove(current_socket)
                    else:
                        self.q.put(msg)

    def recv_file(self):
        pass


if __name__ == '__main__':
    q = queue.Queue()
    soc = ServerCom(1111, q)