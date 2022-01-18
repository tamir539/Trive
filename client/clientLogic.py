import queue
from clientNetwork import ClientCom
import graphic
import threading
import wx
from pubsub import pub
import cprotocol as prot


def check_network_q(network_q):
    '''

    :param q:network queue
    :return: check if there is a new massage
    '''
    while True:
        #get the msg from the network
        msg = network_q.get()
        #do decryption
        #decryption
        #unpack by protocol
        msg_after_unpack = prot.unpack(msg)
        #the command from the server
        command = msg_after_unpack[0]
        #the arguments from the server
        args = msg_after_unpack[1]
        if command == 'send_all_files':
            get_all_files(args)
        elif command == 'download_answer':
            download_answer(args)
        else:
            wx.CallAfter(pub.sendMessage, command, massage = msg)


def check_graphic_q(graphic_q):
    '''

    :param graphic_q:graphic q
    :return: check if there is a new massage
    '''
    print('in')
    func_by_command = {'register': send_register, 'login': send_login}
    while True:
        msg = graphic_q.get()
        flag = msg[0]
        args = msg[1]
        func_by_command[flag](args)
        #wx.CallAfter(pub.sendMessage, command, massage = args[0])


def get_all_files(args):
    '''

    :param args: the files structure from the server
    :return: builds the structure back and deliver to the graphic
    '''
    pass


def download_answer(args):
    '''

    :param args:details for download file
    :return: create new network to recive the file and notify the graphic when finish
    '''
    pass


def start_graphic(graphic_q):
    '''

    :param graphic_q:q to talk with the graphic
    :return: creates the graphic
    '''
    app = wx.App()
    frame = graphic.MyFrame(graphic_q)
    app.MainLoop()


def send_register(args):
    '''

    :param args: all the details for registration
    :return: send registration massage to the server
    '''
    print('in send register')
    email = args[0]
    username = args[1]
    password = args[2]
    #create the msg by the protocol
    msg_by_protocol = prot.create_register_msg(username, password, email)
    #take to encryption
    #encryption
    #send the msg
    network.send_msg(msg_by_protocol)


def send_login(args):
    '''

    :param args: all the details for login
    :return: send login massage to the server
    '''
    username = args[0]
    password = args[1]
    # create the msg by the protocol
    msg_by_protocol = prot.create_login_msg(username, password)
    # take to encryption
    # encryption
    # send the msg
    network.send_msg(msg_by_protocol)

#queue to get massages from the network
network_q = queue.Queue()
#queue to get massages from the graphic
graphic_q = queue.Queue()

network = ClientCom('127.0.0.1', 1111, network_q)


threading.Thread(target= start_graphic, args= (graphic_q, )).start()
threading.Thread(target= check_network_q, args= (network_q, ), daemon=True).start()
threading.Thread(target= check_graphic_q, args= (graphic_q, ), daemon=True).start()

