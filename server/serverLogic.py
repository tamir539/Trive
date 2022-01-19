import queue
import threading
import sprotocol as prot
from serverNetwork import ServerCom
from dataBase import  DB
import hashlib
import smtplib
import random


def check_network_q(network_q):
    '''

    :param q:network queue
    :return: check if there is a new massage
    '''
    func_by_command = {'login': handle_login, 'register': handle_register, 'upload': handle_upload,
                       'download' : handle_download, 'delete': handle_delete, 'add_to_folder': handle_add_to_folder,
                       'create_folder':handle_create_folder, 'change_details': handle_change_details, 'share': handle_share,
                       'change_name': handle_change_file_name, 'forgot_password': handle_forgot_password}
    while True:
        msg = network_q.get()
        #do decryption
        msg_after_unpack = prot.unpack_msg(msg[0])
        #the command that the client requested
        command = msg_after_unpack[0]
        #the parameters the client gave
        args = msg_after_unpack[1]
        #the socket
        args.append(msg[1])
        args.append(msg[2])
        func_by_command[command](args)


def handle_login(args):
    '''

    :param args: args to the login
    :return: check the login and returns answer to the client
    '''
    myDB = DB('Trive')
    print('in handle login')
    username = args[0]
    password = args[1]
    soc = args[2]
    ip = args[3]
    #send username and password to decryption
    hashed_password = myDB.getPasswordOfUser(username)
    answer = 'no'
    if ip in trys_by_ip.keys() and trys_by_ip[ip] == 4:
        network.block_ip(ip)
        answer = 'blocked'
        print(ip, ' blocked')
    elif myDB.check_username_exist(username) and password == hashed_password:#hashlib.md5(password.encode()) == hashed_password:
        answer = 'ok'
        username_connected[soc] = username
        handle_send_all_files(username)
    else:
        if ip not in trys_by_ip.keys():
            trys_by_ip[ip] = 1
        else:
            trys_by_ip[ip] += 1
    #send the answer to encryption
    #encryption
    #build the msg by the protocol
    ans_to_send = prot.create_login_response_msg(answer)
    #send the answer
    network.send_msg(soc, ans_to_send)


def handle_register(args):
    '''

    :param args: args to the register
    :return: check the register and returns answer to the client
    '''
    print('in handle register')

    myDB = DB('Trive')

    username = args[0]
    password = args[1]
    email = args[2]
    soc = args[3]
    # send username and password to decryption
    answer = 'un'
    if myDB.add_user(username, email, password):
        answer = 'ok'
    # send the answer to encryption
    # encryption
    # build the msg by the protocol
    ans_to_send = prot.create_register_response_msg(answer)
    # send the answer
    network.send_msg(soc, ans_to_send)


def handle_change_details(args):
    '''

    :param args:new detailes to update
    :return:try to update the details and return answer to the client
    '''
    #connect to the dataBase
    myDB = DB('Trive')

    #the field to change
    change = args[0].split(':')[0]
    #the new value for the feild
    new_value = args[0].split(':')[1]
    soc = args[1]
    username = username_connected[soc]
    if change == 'email':
        myDB.change_email(username, new_value)
    else:
        myDB.change_password(username, new_value)


def handle_forgot_password(args):
    '''

    :param args:username of the user
    :return: send 1 time password to the email
    '''
    myDB = DB('Trive')

    sender = 'trive933@gmail.com'
    username = args[0]
    if myDB.check_username_exist(username):
        to = myDB.get_email_of_user(username)

        # generate 1 time password
        password = random.randint(1000000, 9999999)

        # update the password in the data base
        myDB.change_password(username, password)

        SUBJECT = "Trive reset password"

        TEXT = f"Your 1 time password is: {password}"

        message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sender, to, SUBJECT, TEXT)

        send = smtplib.SMTP('smtp.gmail.com', 587)
        send.ehlo()
        send.starttls()
        send.login(sender, 'Triveamir539')
        send.sendmail(sender, to, password)  # {password}')
        print('email Sent')


def handle_send_all_files(username):
    '''

    :param username:username
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



#queue to get massages from the network
network_q = queue.Queue()
trys_by_ip = {} #ip -> times that tryd to login from this ip

network = ServerCom(1111, network_q)
username_connected = {}     #socket -> the username that are now connected

threading.Thread(target= check_network_q, args= (network_q, )).start()
