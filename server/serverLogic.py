import queue
import threading
import sprotocol as prot
from serverNetwork import ServerCom


def check_network_q(network_q):
    '''

    :param q:network queue
    :return: check if there is a new massage
    '''
    func_by_command = {'login': handle_login, 'register': handle_register, 'send_all_files': handle_send_all_files, 'upload': handle_upload,
                       'download' : handle_download, 'delete': handle_delete, 'add_to_folder': handle_add_to_folder,
                       'create_folder':handle_create_folder, 'change_details': handle_change_details, 'share': handle_share,
                       'change_name': handle_change_file_name, 'forgot_password': handle_forgot_password}
    while True:
        msg = network_q.get()
        #do decryption
        msg_after_unpack = prot.unpack_msg(msg[0])
        command = msg_after_unpack[0]
        args = msg_after_unpack[1]
        func_by_command[command](args)


def handle_login(args):
    '''

    :param args: args to the login
    :return: check the login and returns answer to the client
    '''
    print('in handle login')



def handle_register(args):
    '''

    :param args: args to the register
    :return: check the register and returns answer to the client
    '''
    print('in handle register')


def handle_send_all_files(args):
    '''

    :param args:username
    :return: send all his files to the client
    '''


def handle_upload(args):
    '''

    :param args: args to the upload
    :return: recive the file and return answer to the client
    '''
    pass


def handle_download(args):
    '''

    :param args:relevante for the download
    :return: send the file to the client
    '''


def handle_delete(args):
    '''

    :param args:file to delete
    :return: try to delete the file and retuirn answer to the client
    '''
    pass


def handle_add_to_folder(args):
    '''

    :param args: file path and folder path
    :return: try to add the file to the folder and return answer to the client
    '''


def handle_create_folder(args):
    '''

    :param args:path to create the folder in
    :return: try to create the folder and return answer to the client
    '''


def handle_change_details(args):
    '''

    :param args:new detailes to update
    :return:try to update the details and return answer to the client
    '''


def handle_share(args):
    '''

    :param args:file to share, username to share with
    :return: try to share the file and return answer to the client
    '''


def handle_change_file_name(args):
    '''

    :param args:file path, his new name
    :return: try to rename the file and return answer to the client
    '''


def handle_forgot_password(args):
    '''

    :param args:email of the user
    :return: send 1 time password to the email
    '''

#queue to get massages from the network
network_q = queue.Queue()

network = ServerCom(1111,network_q)

threading.Thread(target= check_network_q, args= (network_q, )).start()