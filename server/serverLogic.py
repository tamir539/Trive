import queue
import threading
import sprotocol as prot
from serverNetwork import ServerCom
from dataBase import DB
import hashlib
import smtplib
import random
import Sfile
import os
from Encryption import AESCipher
from settings import TRIVE_LOCATION as trive_location
from settings import FILES_KEY as files_key
#finish comments!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def create_trive_directory(path):
    '''

    :return:create the Trive location in the path
    '''
    try:
        os.makedirs(path)
    except:
        pass


def check_network_q(network_q):
    '''

    :param network_q:network queue
    :return: check if there is a new massage
    '''
    func_by_command = {'login': handle_login, 'register': handle_register, 'upload_request': handle_upload_request,
                       'download' : handle_download, 'delete': handle_delete, 'add_to_folder': handle_add_to_folder,
                       'create_folder': handle_create_folder, 'change_details': handle_change_details,
                       'share': handle_share, 'change_name': handle_change_file_name,
                       'forgot_password': handle_forgot_password, 'edit': handle_edit}

    while True:
        msg = network_q.get()
        #finish reciving file
        if msg[0] == 'upload':
            handle_upload_status(msg[1:])
        #set key
        elif msg[0] == 'key':
            set_key(msg[1], msg[2])
        #client disconnected
        elif msg[0] == 'disconnected':
            if msg[1] in list(username_connected.keys()):
                del username_connected[msg[1]]
        #download finish -> the port released
        elif msg[0] == 'close_port':
            taken_ports.remove(msg[1])
        else:
            ip = msg[1]
            msg = msg[0]
            decrypted_msg = key_by_ip[ip].decrypt(msg)
            msg_after_unpack = prot.unpack_msg(decrypted_msg)
            #the command that the client requested
            command = msg_after_unpack[0]
            #the parameters the client gave
            args = msg_after_unpack[1]
            #the ip
            args.append(ip)
            func_by_command[command](args)


def handle_login(args):
    '''

    :param args: args to the login
    :return: check the login and returns answer to the client
    '''
    my_db = DB('Trive')
    username = args[0]
    password = args[1]
    ip = args[2]
    #send username and password to decryption
    hashed_password = my_db.get_password_of_user(username)
    answer = 'no'
    #check if the ip is blocked
    if ip in trys_by_ip.keys() and trys_by_ip[ip] == 4:
        network.block_ip(ip)
        answer = 'blocked'
    #ceck if the user is already connected from another device
    elif username in list(username_connected.values()):
        answer = 'ac'
    elif my_db.check_username_exist(username) and hashlib.md5(password.encode()).hexdigest() == hashed_password:
        answer = 'ok' + ',' + my_db.get_email_of_user(username)
        username_connected[ip] = username
        #send email alert when the ip isnt identify
        if not my_db.check_ip_exist_for_username(username, ip):
            threading.Thread(target=send_email, args= (f'New connection was detected to your Trive account from ip: {ip}', my_db.get_email_of_user(username), )).start()
        handle_send_all_files(username, ip)
        my_db.add_ip_for_username(username, ip)

    else:
        if ip not in trys_by_ip.keys():
            trys_by_ip[ip] = 1
        else:
            trys_by_ip[ip] += 1
    #build the msg by the protocol
    ans_to_send = prot.create_login_response_msg(answer)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(ans_to_send)
    #send the answer
    network.send_msg(ip, encrypted_msg)


def send_email(msg, to):
    '''

    :param msg:msg to send
    :param to: send to
    :return: send email with message to to
    '''
    by = 'Trive933@gmail.com'

    to = [to]

    subject = "New connection was detected"

    text = msg

    message = """\
            From: %s
            %s

            %s
            """ % (by, subject, text)

    try:
        serv = smtplib.SMTP('smtp.gmail.com', 587)
        serv.ehlo()
        serv.starttls()
        serv.login(by, 'Triveamir539')
        serv.sendmail(by, to, message)
        serv.close()
    except Exception as e:
        print(str(e))
        print('Something went wrong...')


def handle_register(args):
    '''

    :param args: args to the register
    :return: check the register and returns answer to the client
    '''
    my_db = DB('Trive')

    username = args[0]
    password = hashlib.md5(args[1].encode()).hexdigest()
    email = args[2]
    ip = args[3]
    # send username and password to decryption
    answer = 'un'
    if my_db.add_user(username, email, password):
        answer = 'ok'
        try:
            os.makedirs(f'{trive_location}\\{username}\\shared')
            os.makedirs(f'{trive_location}\\{username}\\recycle')
        except:
            pass
    # build the msg by the protocol
    ans_to_send = prot.create_register_response_msg(answer)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(ans_to_send)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def handle_change_details(args):
    '''

    :param args:new detailes to update
    :return:try to update the details and return answer to the client
    '''
    #connect to the dataBase
    my_db = DB('Trive')

    #the field to change
    change = args[0].split(':')[0]
    #the new value for the feild
    new_value = args[0].split(':')[1]
    ip = args[1]
    username = username_connected[ip]
    if change == 'email':
        ans = my_db.change_email(username, new_value)
    else:
        password = hashlib.md5(new_value.encode()).hexdigest()
        ans = my_db.change_password(username, password)

    ans_to_send = prot.create_change_detail_response_msg(ans)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(ans_to_send)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def handle_forgot_password(args):
    '''

    :param args:username of the user
    :return: send 1 time password to the email
    '''
    my_db = DB('Trive')

    username = args[0]
    if my_db.check_username_exist(username):

        by = 'Trive933@gmail.com'

        to = [my_db.get_email_of_user(username)]

        subject = "New password"

        password = str(random.randint(10000, 99999))
        my_db.change_password(username, hashlib.md5(password.encode()).hexdigest())

        text = f'Your new password is: {password}'

        message = """\
        From: %s
        Subject: %s

        %s
        """ % (by, subject, text)

        try:
            serv = smtplib.SMTP('smtp.gmail.com', 587)
            serv.ehlo()
            serv.starttls()
            serv.login(by, 'Triveamir539')
            serv.sendmail(by, to, message)
            serv.close()
        except Exception as e:
            print(str(e))
            print('Something went wrong...')


def handle_send_all_files(username, ip):
    '''

    :param username:username
    :param ip: ip of the user
    :return: send all his files to the client
    '''
    msg_by_protocol = prot.pack_file_names(trive_location + '\\' + username)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def handle_upload_status(args):
    '''

    :param args: args to the upload
    :return: recive the file and return answer to the client
    '''
    status, edit, encrypted_path, file_name, port, ip = args
    encrypted_path = encrypted_path  + '\\' + file_name
    if not edit:
        msg_by_protocol = prot.create_upload_file_response_msg(status+','+file_name)
        # send the answer to encryption
        encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
        # send the answer
        network.send_msg(ip, encrypted_msg)
    if status == 'ok':
        #decrypt the file with the client key
        key_by_ip[ip].decrypt_file(encrypted_path)
        #encrypt the file with the server files key
        k = AESCipher(files_key)
        k.encrypt_file(encrypted_path)
    taken_ports.remove(port)


def handle_upload_request(args):
    '''

    :param args:ip
    :return: create server upload and send the new port to the client
    '''
    edit = args[0]
    if edit == 'edit':
        edit = True
    else:
        edit = False
    ip = args[1]
    #generate new port to upload server
    port = random.randint(1000, 65000)
    while port in taken_ports:
        port = random.randint(1000, 65000)

    taken_ports.append(port)

    msg_by_protocol = prot.create_upload_file_response_port_msg(str(port))
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)
    ServerCom(port, network_q, upload_server= True, edit_server=edit)


def handle_download(args):
    '''

    :param args:relevante for the download
    :return: send the file to the client
    '''
    ip = args[1]
    path = args[0]

    #length of the file to send
    length = Sfile.get_file_length(path)

    # generate new port for the download server
    port = random.randint(1000, 65000)
    while port in taken_ports:
        port = random.randint(1000, 65000)

    file_name = args[0][1:]

    msg_by_protocol = prot.create_download_response_msg(str(length), str(port), file_name)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)

    q = queue.Queue()

    send_netwotk = ServerCom(port, q, download_server=True)

    #decrypt the file with the server files's key
    k = AESCipher(files_key)
    k.decrypt_file(path)

    #encrypt the file with the key of the client
    key_by_ip[ip].encrypt_file(path)

    #send the file
    threading.Thread(target = send_netwotk.send_file, args= (path, key_by_ip[ip], k )).start()


def handle_edit(args):
    '''

    :param args:relevante for the download
    :return: send the file to the client
    '''
    ip = args[1]
    path = args[0]

    length = Sfile.get_file_length(path)

    #generate new port for the download server
    port = random.randint(1000, 65000)
    while port in taken_ports:
        port = random.randint(1000, 65000)


    msg_by_protocol = prot.create_edit_response_msg(str(length), str(port), path)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)
    q = queue.Queue()
    send_netwotk = ServerCom(port, q, download_server=True)

    # decrypt the file
    k = AESCipher(files_key)
    k.decrypt_file(path)

    # encrypt the file with the key of the client
    key_by_ip[ip].encrypt_file(path)

    #send the file
    threading.Thread(target=send_netwotk.send_file, args=(path, key_by_ip[ip], k)).start()


def handle_delete(args):
    '''

    :param args:file to delete
    :return: try to delete the file and retuirn answer to the client
    '''
    #path of the file to delete
    path = args[0]
    #name of the file to delete
    file_name = path[path.rindex('\\') + 1:]
    ip = args[1]

    ans = Sfile.delete_file(path, username_connected[ip])
    msg_by_protocol = prot.create_delete_file_response_msg(ans + ',' + file_name)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)
    if ans == 'ok':
        handle_send_all_files(username_connected[ip], ip)


def handle_add_to_folder(args):
    '''

    :param args: file path and folder path
    :return: try to add the file to the folder and return answer to the client
    '''
    #path of the file to copy
    file_to_copy = args[0]
    #folder path to copy to
    copy_to = args[1]
    ip = args[2]

    ans = Sfile.move_file(file_to_copy, copy_to)
    msg_by_protocol = prot.create_insert_file_to_folder_response_msg(ans)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)
    handle_send_all_files( username_connected[ip], ip)


def handle_create_folder(args):
    '''

    :param args:path to create the folder in
    :return: try to create the folder and return answer to the client
    '''
    #path of the new folder
    path = args[0]
    ip = args[1]

    ans = Sfile.create_folder(path)
    msg_by_protocol = prot.create_create_folder_response_msg(ans)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def handle_share(args):
    '''

    :param args:file to share, username to share with
    :return: try to share the file and return answer to the client
    '''
    path = args[0]
    username = args[1]
    ip = args[2]
    my_db = DB('Trive')
    ans = 'no'
    if my_db.check_username_exist(username):
        ans = Sfile.share_file(trive_location, path, username)
    msg_by_protocol = prot.create_share_file_response_msg(ans)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def handle_change_file_name(args):
    '''

    :param args:file path, his new name
    :return: try to rename the file and return answer to the client
    '''
    path = args[0]
    now_name = path[path.rindex('\\') + 1:]
    new_name = args[1]
    ip = args[2]

    ans = Sfile.rename_file(path, new_name)
    msg_by_protocol = prot.create_change_file_name_response_msg(ans+','+now_name+','+new_name)
    # send the answer to encryption
    encrypted_msg = key_by_ip[ip].encrypt(msg_by_protocol)
    # send the answer
    network.send_msg(ip, encrypted_msg)


def set_key(key, ip):
    '''

    :param key:string key to create aes key
    :param ip: ip of theclient
    :return: add the key to the "key_by_ip"
    '''
    aes_key = AESCipher(key)
    key_by_ip[ip] = aes_key


create_trive_directory(trive_location)

#queue to get massages from the network
network_q = queue.Queue()
#ip -> times that tryd to login from this ip
trys_by_ip = {}
#all the taken ports
taken_ports = []
# client ip -> aes key
key_by_ip = {}


network = ServerCom(1111, network_q)
#ip -> the username that are now connected
username_connected = {}

threading.Thread(target= check_network_q, args= (network_q, )).start()
