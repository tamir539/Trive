'''
all the protocol functions of the cient
'''


def unpack(msg):
    '''

    :param msg:msg from the server
    :return: unpack the massage by the protocol and returns tuple with the command and the parameters to the client
    '''
    command_by_code = {'02': 'login', '03': 'register', '04': 'get_all_files', '05': 'upload',
                       '06': 'download', '07': 'delete', '08': 'add_to_folder', '09': 'create_folder',
                       '10': 'change_details', '11': 'share', '13': 'rename', '14': 'forgot_password',
                       '16': 'upload_port', '17': 'edit'}
    code = msg[:2]
    msg = msg[2:]
    args = msg.split('&')
    return command_by_code[code], args


def create_login_msg(username, password):
    '''

    :param username:username
    :param password: password
    :return: creates the massage by the protocol
    '''
    code = '02'
    msg = code + username + '&' + password
    return msg


def create_register_msg(username, password, email):
    '''

    :param username:username
    :param password: password
    :param email: email
    :return: creates the massage by the protocol
    '''
    code = '03'
    msg = code + username + '&' + password + '&' + email
    return msg


def create_all_file_recive_msg(ans):
    '''

    :param ans:answer
    :return: creates the massage by the protocol
    '''
    code = '04'
    msg = code + ans
    return msg


def create_upload_request_file_msg(edit = False):
    '''

    :return: creates the massage by the protocol
    '''
    code = '16'
    if edit:
        code += 'edit'
    return code


def create_upload_file_msg(file_new_path, file_len, file_name):
    '''

    :param file_name: name of the file
    :param file_new_path: where to put the file in the server
    :param file_len: file length
    :return: creates the massage by the protocol
    '''
    code = '05'
    msg = code + str(file_len) + '&' + file_new_path + '&' + file_name
    return msg


def create_download_file_request_msg(file_path):
    '''

    :param file_path: file path in the server
    :return: creates the massage by the protocol
    '''
    code = '06'
    msg = code + file_path
    return msg


def create_delete_file_request_msg(file_path):
    '''

    :param file_path: file path in the server
    :return: creates the massage by the protocol
    '''
    code = '07'
    msg = code + file_path
    return msg


def create_add_file_to_folder_request_msg(file_path, folder_path):
    '''

    :param file_path: file path in the server
    :param folder_path: folder path in the server
    :return: creates the massage by the protocol
    '''
    code = '08'
    msg = code + file_path + '&' + folder_path
    return msg


def create_create_folder_request_msg(folder_path):
    '''

    :param folder_path: folder path in the server
    :return: creates the massage by the protocol
    '''
    code = '09'
    msg = code + folder_path
    return msg


def create_change_details_request_msg(new_value):
    '''

    :param new_value: the new value
    :return: creates the massage by the protocol
    '''
    code = '10'
    msg = code + new_value
    return msg


def create_share_file_request_msg(file_path, username):
    '''

    :param file_path: file path in the server
    :param username: username to share with
    :return: creates the massage by the protocol
    '''
    code = '11'
    msg = code + file_path + '&' + username
    return msg


def create_change_file_name_request_msg(file_path, new_name):
    '''

    :param file_path: file path in the server
    :param file_name: the new file name
    :return: creates the massage by the protocol
    '''
    code = '13'
    msg = code + file_path + '&' + new_name
    return msg


def create_edit_file_request_msg(path):
    '''

    :param path:path to the file
    :return: creates and return the message by the protocol
    '''
    code = '17'
    msg = code + path
    return msg


def create_forgot_password_request_msg(email):
    '''

    :param: email
    :return:create the massage by the protocol
    '''
    code = '14'
    msg = code+email
    return msg

