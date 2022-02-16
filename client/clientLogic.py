import queue
from clientNetwork import ClientCom
import graphic
import threading
import wx
from pubsub import pub
import cprotocol as prot
import os
import psutil
from Encryption import AESCipher
from settings import SERVER_IP as server_ip
import time
import win32con
import win32file

class Logic:
    def __init__(self):

        self.upload_path = ''
        self.upload_server_path = ''
        self.file_name = ''
        self.key = None

        # queue to get massages from the self.network
        self.network_q = queue.Queue()
        # queue to get massages from the graphic
        graphic_q = queue.Queue()

        self.network = ClientCom(server_ip, 1111, self.network_q)
        try:
            os.makedirs('C:\\Trive_uploads')
        except:
            pass
        threading.Thread(target=self.start_graphic, args=(graphic_q,)).start()
        threading.Thread(target=self.check_network_q, args=(self.network_q,), daemon=True).start()
        threading.Thread(target=self.check_graphic_q, args=(graphic_q,), daemon=True).start()
        
    def check_network_q(self, network_q):
        '''
    
        :param q:self.network queue
        :return: check if there is a new massage
        '''
        while True:
            #get the msg from the self.network
            msg = network_q.get()
            if type(msg) is str and msg.startswith('key'):
                key_str = msg.split('-')[1]
                self.key = AESCipher(key_str)
            else:
                if msg == 'disconnect':
                    pass
                elif msg == 'logout':
                    pass
                else:
                    #do decryption
                    decrypted_msg = self.key.decrypt(msg)
                    #unpack by protocol
                    msg_after_unpack = prot.unpack(decrypted_msg)
                    #the command from the server
                    command = msg_after_unpack[0]
                    #the arguments from the server
                    args = msg_after_unpack[1]
                    if command == 'upload_port':
                        self.upload(args[0])
                    elif command == 'download':
                        threading.Thread(target= self.download_answer, args = (args, )).start()
                    elif command == 'edit':
                        threading.Thread(target=self.edit_answer, args=(args,)).start()
                    else:
                        wx.CallAfter(pub.sendMessage, command, answer = args[0])

    def check_graphic_q(self, graphic_q):
        '''
    
        :param graphic_q:graphic q
        :return: check if there is a new massage
        '''
        func_by_command = {'register': self.send_register, 'login': self.send_login, 'forgot_password': self.send_forgot_password, 'change_detail': self.send_change_detail,
                           'download': self.send_download, 'upload': self.send_upload_request, 'share': self.send_share, 'add_to_folder': self.send_add_to_folder, 'rename': self.send_rename,
                           'delete': self.send_delete, 'create_folder': self.send_create_folder, 'edit': self.handle_edit, 'logout': self.send_logout}
        while True:
            flag, args = graphic_q.get()
            func_by_command[flag](args)
            #wx.CallAfter(pub.sendMessage, command, massage = args[0])

    def start_graphic(self, graphic_q):
        '''
    
        :param graphic_q:q to talk with the graphic
        :return: creates the graphic
        '''
        app = wx.App()
        frame = graphic.MyFrame(graphic_q)
        app.MainLoop()
        #kill all the threads
        self.finish()
    
    def send_register(self, args):
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
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_logout(self, args):
        '''

        :return:send logout messgae to the server
        '''
        # msg_by_protocol = prot.create_logout_msg()
        # encrypted_msg = self.key.encrypt(msg_by_protocol)
        # self.network.send_msg(encrypted_msg)
        pass

    def send_login(self, args):
        '''
    
        :param args: all the details for login
        :return: send login massage to the server
        '''
        username = args[0]
        password = args[1]
        # create the msg by the protocol
        msg_by_protocol = prot.create_login_msg(username, password)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def handle_edit(self, args):
        '''

        :param args:path to the file to edit
        :return:
        '''
        file_path = args[0]

        msg_by_protocol = prot.create_edit_file_request_msg(file_path)

        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_forgot_password(self, args):
        '''
    
        :param args: email for the 1 time password
        :return: send forgot_password massage to the server
        '''
        email = args[0]
        # create the msg by the protocol
        msg_by_protocol = prot.create_forgot_password_request_msg(email)
        # take to encryption
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_change_detail(self, args):
        '''
    
        :param args:the new email or password
        :return: send the server msg to chande detail
        '''
        new_value = args[0]
        #create the msg by the protocol
        msg_by_protocol = prot.create_change_details_request_msg(new_value)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_download(self, args):
        '''
    
        :param args:virtual file path to file
        :return: send request to download that file
        '''
        path = args[0]
    
        msg_by_protocol = prot.create_download_file_request_msg(path)

        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_rename(self, args):
        '''
    
        :param args:virtual file path to file, new name to this file
        :return: send request to rename that file
        '''
        path = args[0]
        new_name = args[1]
        msg_by_protocol = prot.create_change_file_name_request_msg(path, new_name)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_upload_request(self, args, edit = False):
        '''
    
        :param args:file path to file
        :return: send request to upload that file
        '''
        #path in this computer
        self.upload_path = args[0]
        self.file_name = self.upload_path[self.upload_path.rindex('\\') + 1:]
        #path to upload in the server
        self.upload_server_path = args[1]
        msg_by_protocol = prot.create_upload_request_file_msg(edit)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def upload(self, port):
        '''
    
        :param port: server port
        :return: upload the file to the server in the port
        '''
        client_upload = ClientCom(server_ip, int(port), self.network_q)
        encrypted_path = self.key.encrypt_file(self.upload_path, 'C:\\Trive_uploads\\')
        threading.Thread(target=client_upload.send_file, args= (encrypted_path, self.upload_server_path, self.file_name, )).start()

    def send_add_to_folder(self, args):
        '''
    
        :param args:virtual file path to file, virtual file path to folder
        :return: send request to add that file to folder
        '''
        file_to_copy = args[0]
        copy_to = args[1]
    
        msg_by_protocol = prot.create_add_file_to_folder_request_msg(file_to_copy, copy_to)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)
    
    def send_share(self, args):
        '''
    
        :param args:virtual file path to file, username to share with
        :return: send request to share that file
        '''
        path = args[0]
        username = args[1]
    
        msg_by_protocol = prot.create_share_file_request_msg(path, username)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_delete(self, args):
        '''
    
        :param args:virtual file path to file
        :return: send request to delete that file
        '''
        path = args[0]
        msg_by_protocol = prot.create_delete_file_request_msg(path)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def send_create_folder(self, args):
        '''
    
        :param args:virtual path to create the folder
        :return: send request to create the folder
        '''
        path = args[0]
        msg_by_protocol = prot.create_create_folder_request_msg(path)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        # send the msg
        self.network.send_msg(msg_encrypted)

    def download_answer(self, args):
        '''
    
        :param args:details for download file
        :return: create new self.network to recive the file and notify the graphic when finish
        '''
        port = int(args[0])
        length = int(args[1])
        path = args[2]
        file_name = path[path.rindex('\\') + 1:]
        ready_q = queue.Queue()     #get massage in this q when the download finished
        download_network = ClientCom(server_ip, port, ready_q, True)
        download_network.recv_file(length, file_name, self.key)
        while True:
            finish = ready_q.get()
            wx.CallAfter(pub.sendMessage, 'finish_download', ans=finish)

    def edit_answer(self, args):
        '''

        :param args:details for download server
        :return: download the file, open it and check for changes
        '''
        port = int(args[0])
        length = int(args[1])
        path = args[2]
        file_name = path[path.rindex('\\') + 1:]
        ready_q = queue.Queue()  # get massage in this q when the download finished
        try:
            os.makedirs('C:\\hidden')
        except:
            pass
        download_network = ClientCom(server_ip, port, ready_q, True)
        download_network.recv_file(length, file_name, self.key, path = 'C:\\hidden')
        finish = ready_q.get()
        if finish:
            threading.Thread(target = self.follow_file, args=(f'C:\\hidden\\{file_name}', path)).start()

    def follow_file(self, file_path, server_path):
        '''

        :param path:path for file to  follow
        :param server_path: the path of the file in the server
        :return: upload the file to the server in each change
        '''
        self.open_file(file_path)
        _file_list_dir = 1
        # Create a watcher handle
        _h_dir = win32file.CreateFile(file_path[:file_path.rindex('\\')], _file_list_dir, win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE |  win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
        while 1:
            #results = win32file.ReadDirectoryChangesW(_h_dir, 1024, True, win32con.FILE_NOTIFY_CHANGE_SIZE | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE, None, None)
            results = win32file.ReadDirectoryChangesW(
                _h_dir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                win32con.FILE_NOTIFY_CHANGE_SIZE |
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            for _action, _file in results:
                if _action == 4 and 'docx' in _file:
                    server_path_without_name = server_path[:server_path.rindex('\\')]
                    self.send_upload_request([file_path, server_path_without_name], True)
                if _action == 2 and 'docx' in _file:
                    break


    def open_file(self, file_path):
        '''

        :param file_path:path of the file to open
        :return: open the file
        '''
        file_typ = file_path.split('.')[1]
        #file_name = file_typ[file_path.rstrip('\\') + 1:]
        notepad = ['py', 'txt', 'java', 'asm']
        word = ['doc', 'docx']
        excel = ['xlsx']
        power_point = ['pptm']
        if file_typ in notepad:
            #open notepad
            osCommandString = f"notepad.exe {file_path}"
            os.system(osCommandString)
        elif file_typ in word or 1 == 1:
            os.system(f'start {file_path}')
        elif file_typ in excel:
            #open excel
            pass
        elif file_typ in power_point:
            #open powerpoint
            pass

    def finish(self):
        '''
    
        :return: close all the threads and exit the program
        '''
        parent_pid = os.getpid()
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            child.kill()
        parent.kill()



Logic()
