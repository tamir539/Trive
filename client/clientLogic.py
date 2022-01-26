import queue
from clientNetwork import ClientCom
import graphic
import threading
import wx
from pubsub import pub
import cprotocol as prot
import os
import psutil
import time


global upload_server_path
global upload_path
global file_name
upload_path = ''
upload_server_path = ''
file_name = ''

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
        if command == 'upload_port':
            upload(args[0])
        elif command == 'download':
            threading.Thread(target= download_answer, args = (args, )).start()
        else:
            wx.CallAfter(pub.sendMessage, command, answer = args[0])


def check_graphic_q(graphic_q):
    '''

    :param graphic_q:graphic q
    :return: check if there is a new massage
    '''
    func_by_command = {'register': send_register, 'login': send_login, 'forgot_password': send_forgot_password, 'change_detail': send_change_detail,
                       'download': send_download, 'upload': send_upload_request, 'share': send_share, 'add_to_folder': send_add_to_folder, 'rename': send_rename,
                       'delete': send_delete, 'create_folder': send_create_folder}
    while True:
        msg = graphic_q.get()
        flag = msg[0]
        args = msg[1]
        func_by_command[flag](args)
        #wx.CallAfter(pub.sendMessage, command, massage = args[0])


def start_graphic(graphic_q):
    '''

    :param graphic_q:q to talk with the graphic
    :return: creates the graphic
    '''
    app = wx.App()
    frame = graphic.MyFrame(graphic_q)
    app.MainLoop()
    #kill all the threads
    finish()


def send_register(args):
    '''

    :param args: all the details for registration
    :return: send registration massage to the server
    '''

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


def send_forgot_password(args):
    '''

    :param args: email for the 1 time password
    :return: send forgot_password massage to the server
    '''
    email = args[0]
    # create the msg by the protocol
    msg_by_protocol = prot.create_forgot_password_request_msg(email)
    # take to encryption
    # encryption
    # send the msg
    network.send_msg(msg_by_protocol)


def send_change_detail(args):
    '''

    :param args:the new email or password
    :return: send the server msg to chande detail
    '''
    new_value = args[0]
    #create the msg by the protocol
    msg_by_protocol = prot.create_change_details_request_msg(new_value)
    #take to encryption
    #decryption
    network.send_msg(msg_by_protocol)


def send_download(args):
    '''

    :param args:virtual file path to file
    :return: send request to download that file
    '''
    path = args[0]

    msg_by_protocol = prot.create_download_file_request_msg(path)
    #encryption
    network.send_msg(msg_by_protocol)


def send_rename(args):
    '''

    :param args:virtual file path to file, new name to this file
    :return: send request to rename that file
    '''
    path = args[0]
    new_name = args[1]
    #encryption
    msg_by_protocol = prot.create_change_file_name_request_msg(path, new_name)
    network.send_msg(msg_by_protocol)


def send_upload_request(args):
    '''

    :param args:file path to file
    :return: send request to upload that file
    '''
    global upload_path
    global upload_server_path
    global file_name

    #path in this computer
    upload_path = args[0]
    file_name = upload_path[upload_path.rindex('\\') + 1:]
    #path to upload in the server
    upload_server_path = args[1]
    msg_by_protocol = prot.create_upload_request_file_msg()
    #encryption
    network.send_msg(msg_by_protocol)


def upload(port):
    global upload_path
    global upload_server_path
    global file_name

    client_upload = ClientCom(server_ip, int(port), network_q)
    time.sleep(1)
    client_upload.send_file(upload_path, upload_server_path, file_name)


def send_add_to_folder(args):
    '''

    :param args:virtual file path to file, virtual file path to folder
    :return: send request to add that file to folder
    '''


def send_share(args):
    '''

    :param args:virtual file path to file, username to share with
    :return: send request to share that file
    '''
    path = args[0]
    username = args[1]

    msg_by_protocol = prot.create_share_file_request_msg(path, username)
    #encryption
    network.send_msg(msg_by_protocol)



def send_delete(args):
    '''

    :param args:virtual file path to file
    :return: send request to delete that file
    '''
    path = args[0]
    msg_by_protocol = prot.create_delete_file_request_msg(path)
    #encryption
    network.send_msg(msg_by_protocol)



def send_create_folder(args):
    '''

    :param args:virtual path to create the folder
    :return: send request to create the folder
    '''
    path = args[0]
    msg_by_protocol = prot.create_create_folder_request_msg(path)
    #encryption
    network.send_msg(msg_by_protocol)


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
    port = int(args[0])
    length = int(args[1])
    path = args[2]
    file_name = path[path.rindex('\\') + 1:]
    ready_q = queue.Queue()     #get massage in this q when the download finished
    download_network = ClientCom(server_ip, port, ready_q, True)
    download_network.recv_file(length, file_name)

    while True:
        finish = ready_q.get()
        wx.CallAfter(pub.sendMessage, 'finish_download', ans=finish)


def finish():
    '''

    :return: close all the threads and exit the program
    '''
    parent_pid = os.getpid()
    parent = psutil.Process(parent_pid)
    for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        child.kill()
    parent.kill()


#queue to get massages from the network
network_q = queue.Queue()
#queue to get massages from the graphic
graphic_q = queue.Queue()
server_ip = '127.0.0.1'

has_upload_server = False

file_name_by_port = {}      #download port -> file name




network = ClientCom(server_ip, 1111, network_q)


threading.Thread(target= start_graphic, args= (graphic_q, )).start()
threading.Thread(target= check_network_q, args= (network_q, ), daemon=True).start()
threading.Thread(target= check_graphic_q, args= (graphic_q, ), daemon=True).start()

