import queue
from clientNetwork import ClientCom
import graphic
import threading
import wx
from pubsub import pub

def check_network_q(network_q):
    '''

    :param q:network queue
    :return: check if there is a new massage
    '''
    while True:
        msg = network_q.get()
        #do decryption
        #send to protocol unpack
        wx.CallAfter(pub.sendMessage, 'register_answer', msg)

def check_graphic_q(graphic_q):
    '''

    :param graphic_q:graphic q
    :return: check if there is a new massage
    '''
    print('in')
    while True:
        msg = graphic_q.get()
        print(msg)
        wx.CallAfter(pub.sendMessage, msg[0], massage = msg[1][0])

def start_graphic(graphic_q):
    app = wx.App()
    frame = graphic.MyFrame(graphic_q)
    app.MainLoop()

#queue to get massages from the network
network_q = queue.Queue()
#queue to get massages from the graphic
graphic_q = queue.Queue()

network = ClientCom('127.0.0.1', 1111, network_q)


threading.Thread(target= start_graphic, args= (graphic_q, )).start()
threading.Thread(target= check_network_q, args= (network_q, ), daemon=True).start()
threading.Thread(target= check_graphic_q, args= (graphic_q, ), daemon=True).start()

