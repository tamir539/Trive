import queue
import threading
import sprotocol as prot
from serverNetwork import ServerCom
from dataBase import  DB
import hashlib
import smtplib
import random
import Sfile
import os


def create_Trive_directory(path):
    '''

    :return:
    '''
    try:
        os.makedirs(path)
    except:
        pass



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
        #the ip
        args.append(msg[1])
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
    ip = args[2]
    #send username and password to decryption
    hashed_password = myDB.getPasswordOfUser(username)
    answer = 'no'
    if ip in trys_by_ip.keys() and trys_by_ip[ip] == 4:
        network.block_ip(ip)
        answer = 'blocked'
        print(ip, ' blocked')
    elif myDB.check_username_exist(username) and password == hashed_password:#hashlib.md5(password.encode()) == hashed_password:
        answer = 'ok'
        username_connected[ip] = username
        handle_send_all_files(username, ip)
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
    network.send_msg(ip, ans_to_send)


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
    ip = args[3]
    # send username and password to decryption
    answer = 'un'
    if myDB.add_user(username, email, password):
        answer = 'ok'
        try:
            os.makedirs(f'{trive_location}\\{username}')
        except:
            pass
    # send the answer to encryption
    # encryption
    # build the msg by the protocol
    ans_to_send = prot.create_register_response_msg(answer)
    # send the answer
    network.send_msg(ip, ans_to_send)


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
    ip = args[1]
    username = username_connected[ip]
    if change == 'email':
        ans = myDB.change_email(username, new_value)
    else:
        ans = myDB.change_password(username, new_value)

    msg_by_protocol = prot.create_change_detail_response_msg(ans)

    network.send_msg(ip, msg_by_protocol)

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


def handle_send_all_files(username, ip):
    '''

    :param username:username
    :return: send all his files to the client
    '''
    msg_by_protocol = prot.pack_file_names(trive_location + '\\' + username)
    network.send_msg(ip, msg_by_protocol)


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
    ip = args[1]
    path = args[0]

    length = Sfile.get_file_length(path)

    port = random.randint(1000, 65000)
    while port in taken_ports:
        port = random.randint(1000, 65000)

    file_name = args[0][1:]

    msg_by_protocol = prot.create_download_response_msg(str(length), str(port), file_name)
    #encryption
    network.send_msg(ip, msg_by_protocol)
    q = queue.Queue()



    send_netwotk = ServerCom(port, q)
    send_netwotk.send_file(path)
    print('sent file ', path)




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
    print('handle create folder')
    path = args[0]
    print(path)
    ip = args[1]
    ans = Sfile.create_folder(path)
    answer = prot.create_create_folder_response_msg(ans)
    network.send_msg(ip, answer)


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


#the loaction of all the files
trive_location = 'C:\\Trive'

create_Trive_directory(trive_location)

#queue to get massages from the network
network_q = queue.Queue()
trys_by_ip = {} #ip -> times that tryd to login from this ip
taken_ports = []    #all the taken ports




network = ServerCom(1111, network_q)
username_connected = {}     #ip -> the username that are now connected

threading.Thread(target= check_network_q, args= (network_q, )).start()
