import queue
from clientNetwork import ClientCom
import graphic
import threading
import wx
from pubsub import pub
import cprotocol as prot
import os
from Encryption import AESCipher
from settings import SERVER_IP as server_ip
import win32con
import win32file
import ctypes
import psutil
import time


class Logic:
    '''
    logic of the client
    '''
    def __init__(self):
        '''
            upload path -> path of the file to upload if there is one
            upload_server_path -> place in the server to upload the file to
            file_name -> name of the file that uploading now
            key -> aes key with the server
            network_q - > queue to recive msgs from the network
            graphic_q -> queue to recive msgs from the graphic
            network -> client network object
            frame -> frame of the graphic
        '''
        self.upload_path = ''
        self.upload_server_path = ''
        self.file_name = ''
        self.key = None

        self.network_q = queue.Queue()

        self.graphic_q = queue.Queue()

        self.network = ClientCom(server_ip, 1111, self.network_q)

        self.frame = None

        # create folder for the uploads
        try:
            os.makedirs('C:\\Trive_uploads')
            #  Hide folder
            ctypes.windll.kernel32.SetFileAttributesW('C:\\Trive_uploads', 2)
        except:
            pass

        threading.Thread(target=self.start_graphic,).start()
        threading.Thread(target=self.check_network_q, daemon=True).start()
        threading.Thread(target=self.check_graphic_q, daemon=True).start()

    def check_network_q(self):
        '''

        :return: check if there is a new massage
        '''
        while True:
            # get the msg from the self.network
            msg = self.network_q.get()
            if type(msg) is str and msg.startswith('key'):
                key_str = msg.split('-')[1]
                self.key = AESCipher(key_str)
            else:
                if type(msg) is str and msg == 'disconnect':
                    wx.CallAfter(pub.sendMessage, 'disconnect')
                else:
                    # do decryption
                    decrypted_msg = self.key.decrypt(msg)
                    # unpack by protocol
                    msg_after_unpack = prot.unpack(decrypted_msg)
                    # the command and arguments from the server
                    command, args = msg_after_unpack
                    if command == 'upload_port':
                        self.upload(args[0])
                    elif command == 'download':
                        threading.Thread(target= self.download_answer, args = (args, )).start()
                    elif command == 'edit':
                        threading.Thread(target=self.edit_answer, args=(args,)).start()
                    else:
                        # notify the command to the graphic
                        wx.CallAfter(pub.sendMessage, command, answer = args[0])

    def check_graphic_q(self):
        '''

        :return: check if there is a new massage
        '''
        func_by_command = {'register': self.send_register, 'login': self.send_login, 'forgot_password': self.send_forgot_password, 'change_detail': self.send_change_detail,
                           'download': self.send_download, 'upload': self.send_upload_request, 'share': self.send_share, 'add_to_folder': self.send_add_to_folder, 'rename': self.send_rename,
                           'delete': self.send_delete, 'create_folder': self.send_create_folder, 'edit': self.handle_edit}
        while True:

            # recive msg from the graphic
            flag, args = self.graphic_q.get()
            if self.key:
                func_by_command[flag](args)
            else:
                wx.CallAfter(pub.sendMessage, 'disconnect')

    def start_graphic(self):
        '''

        :return: creates the graphic
        '''
        app = wx.App()
        self.frame = graphic.MyFrame(self.graphic_q)
        app.MainLoop()
        # kill all the threads when the graphic closed
        self.finish()

    def send_register(self, args):
        '''

        :param args: all the details for registration
        :return: send registration massage to the server
        '''
        email, username, password = args
        # create the msg by the protocol
        msg_by_protocol = prot.create_register_msg(username, password, email)
        # take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_login(self, args):
        '''

        :param args: all the details for login
        :return: send login massage to the server
        '''
        username = args[0]
        password = args[1]
        #  create the msg by the protocol
        msg_by_protocol = prot.create_login_msg(username, password)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def handle_edit(self, args):
        '''

        :param args:path to the file to edit
        :return:
        '''
        file_path = args[0]
        # create the massage by the protocol
        msg_by_protocol = prot.create_edit_file_request_msg(file_path)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_forgot_password(self, args):
        '''

        :param args: email for the 1 time password
        :return: send forgot_password massage to the server
        '''
        email = args[0]
        #  create the msg by the protocol
        msg_by_protocol = prot.create_forgot_password_request_msg(email)
        #  take to encryption
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_change_detail(self, args):
        '''

        :param args:the new email or password
        :return: send the server msg to chande detail
        '''
        new_value = args[0]
        # create the msg by the protocol
        msg_by_protocol = prot.create_change_details_request_msg(new_value)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_download(self, args):
        '''

        :param args:virtual file path to file
        :return: send request to download that file
        '''
        path = args[0]

        msg_by_protocol = prot.create_download_file_request_msg(path)

        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_rename(self, args):
        '''

        :param args:virtual file path to file, new name to this file
        :return: send request to rename that file
        '''
        path, new_name = args
        msg_by_protocol = prot.create_change_file_name_request_msg(path, new_name)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_upload_request(self, args, edit = False):
        '''

        :param args:file path to file
        :return: send request to upload that file
        '''
        # path in this computer, path to upload in the server
        self.upload_path, self.upload_server_path = args
        self.file_name = self.upload_path[self.upload_path.rindex('\\') + 1:]
        msg_by_protocol = prot.create_upload_request_file_msg(edit)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def upload(self, port):
        '''

        :param port: server port
        :return: upload the file to the server in the port
        '''
        # network to recive file
        client_upload = ClientCom(server_ip, int(port), self.network_q)
        encrypted_path = self.key.encrypt_file(self.upload_path, 'C:\\Trive_uploads\\')
        threading.Thread(target=client_upload.send_file, args= (encrypted_path, self.upload_server_path, self.file_name, )).start()

    def send_add_to_folder(self, args):
        '''

        :param args:virtual file path to file, virtual file path to folder
        :return: send request to add that file to folder
        '''
        file_to_copy, copy_to = args

        msg_by_protocol = prot.create_add_file_to_folder_request_msg(file_to_copy, copy_to)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_share(self, args):
        '''

        :param args:virtual file path to file, username to share with
        :return: send request to share that file
        '''
        path, username = args

        msg_by_protocol = prot.create_share_file_request_msg(path, username)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_delete(self, args):
        '''

        :param args:virtual file path to file
        :return: send request to delete that file
        '''
        path = args[0]
        msg_by_protocol = prot.create_delete_file_request_msg(path)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def send_create_folder(self, args):
        '''

        :param args:virtual path to create the folder
        :return: send request to create the folder
        '''
        path = args[0]
        msg_by_protocol = prot.create_create_folder_request_msg(path)
        #  take to encryption
        msg_encrypted = self.key.encrypt(msg_by_protocol)
        #  send the msg
        self.network.send_msg(msg_encrypted)

    def download_answer(self, args):
        '''

        :param args:details for download file
        :return: create new self.network to recive the file and notify the graphic when finish
        '''
        port, length, path = args
        # port for download server
        port = int(port)
        length = int(length)

        file_name = path[path.rindex('\\') + 1:]
        ready_q = queue.Queue()     # get massage in this q when the download finished
        download_network = ClientCom(server_ip, port, ready_q, file = True)
        download_network.recv_file(length, file_name, self.key)
        while True:
            # wait for download to finish
            finish = ready_q.get()
            wx.CallAfter(pub.sendMessage, 'finish_download', ans=finish)

    def edit_answer(self, args):
        '''

        :param args:details for download server
        :return: download the file, open it and check for changes
        '''
        port, length, path = args
        # port for download server
        port = int(port)
        length = int(length)
        file_name = path[path.rindex('\\') + 1:]
        #  get massage in this q when the download finished
        ready_q = queue.Queue()
        try:
            os.makedirs('C:\\hidden')
            #  Hide folder
            ctypes.windll.kernel32.SetFileAttributesW('C:\\hidden', 2)
        except:
            pass
        download_network = ClientCom(server_ip, port, ready_q, True)
        download_network.recv_file(length, file_name, self.key, path = 'C:\\hidden')
        finish = ready_q.get()

        if finish:
            # check if the file opens in notepad
            if 'txt' in file_name or 'py' in file_name:
                all_notepad_pids = []
                for proc in psutil.process_iter():
                    if 'notepad' in proc.name():
                        all_notepad_pids.append(proc.pid)
                threading.Thread(target = self.follow_notepad_file, args= (all_notepad_pids, f'C:\\hidden\\{file_name}', path )).start()
            else:
                threading.Thread(target = self.follow_office_file, args=(f'C:\\hidden\\{file_name}', path)).start()

    def follow_notepad_file(self, all_notepad_pids, file_path, server_path):
        '''

        :param file_path: path of the file that editing
        :param server_path: path for the upload
        :param all_notepad_pids: all the pids of the files that were opened in notepad
        :return: upload the file to the server in each change
        '''
        # open the file
        threading.Thread(target= self.open_file, args=(file_path, )).start()

        server_path_without_name = server_path[:server_path.rindex('\\')]

        time.sleep(0.1)
        now_notepad_pids = []

        for proc in psutil.process_iter():
            if 'notepad' in proc.name():
                now_notepad_pids.append(proc.pid)

        # get the pid of the proccess
        pid = list(set(now_notepad_pids) - set(all_notepad_pids))[0]

        last_change = os.path.getmtime(file_path)

        while True:
            # check if the file updated
            if os.path.getmtime(file_path) != last_change:
                last_change = os.path.getmtime(file_path)
                # upload the file
                self.send_upload_request([file_path, server_path_without_name], True)

            if not psutil.pid_exists(pid):
                # the file closed -> close the monitor
                self.frame.finish_edit()
                os.remove(file_path)
                break

    def follow_office_file(self, file_path, server_path):
        '''

        :param file_path:path for file to  follow
        :param server_path: the path of the file in the server
        :return: upload the file to the server in each change
        '''
        # open the file
        self.open_file(file_path)
        file_typ = file_path.split('.')[1]
        _file_list_dir = 1
        #  Create a watcher handle
        _h_dir = win32file.CreateFile(file_path[:file_path.rindex('\\')], _file_list_dir, win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE |  win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None)
        while 1:
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
                if _action == 4 and file_typ in _file:
                    #  the file saved -> upload to the server
                    server_path_without_name = server_path[:server_path.rindex('\\')]
                    self.send_upload_request([file_path, server_path_without_name], True)
                if _action == 2 and file_typ in _file:
                    #  the file closed -> close the monitor
                    self.frame.finish_edit()
                    os.remove(file_path)
                    break

    def open_file(self, file_path):
        '''

        :param file_path:path of the file to open
        :return: open the file
        '''
        file_typ = file_path.split('.')[1]

        notepad = ['py', 'txt', 'java', 'asm']
        office = ['doc', 'docx', 'pptm', 'xlsx']

        if file_typ in notepad:
            # open notepad
            os.system(f'notepad.exe {file_path}')
        elif file_typ in office:
            os.system(f'start {file_path}')

    def finish(self):
        '''

        :return: close all the threads and exit the program
        '''
        parent_pid = os.getpid()
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):  #  or parent.children() for recursive=False
            child.kill()
        parent.kill()

if __name__ == '__main__':
    Logic()
