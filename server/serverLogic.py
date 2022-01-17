import queue
import threading


def check_network_q(network_q):
    '''

    :param q:network queue
    :return: check if there is a new massage
    '''
    while True:
        msg = network_q.get()
        #do decryption
        #send to protocol unpack
        print('in check_network_q: ', msg)

#queue to get massages from the network
network_q = queue.Queue()

threading.Thread(target= check_network_q, args= (network_q, ), daemon=True).start()