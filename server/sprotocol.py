def create_all_files_msg(msg):
    '''

    :param msg:string that presents all the files of user in structure
    :return: builds and return the msg by the protocol
    '''
    return create_response('04', msg)

def unpack_msg(msg):
    '''

    :param msg:msg from the client
    :return: unpack by the protocol and returns to the main server the msg and the relevants args
    '''
    command_by_code = {'02': 'login', '03': 'register', '04': 'send_all_files', '05': 'upload',
                       '06':'download', '07': 'delete', '08': 'add_to_folder', '09': 'create_folder',
                       '10': 'change_details', '11': 'share', '13': 'change_name', '14': 'forgot_password'}
    #the code of the msg
    code = msg[:2]
    msg = msg[2:]
    #all the arguments of the msg
    args = msg.split('&')
    return command_by_code[code], args

def create_download_response_msg(file_len, port):
    '''

    :param file_len:length of file
    :param port: port for the download server
    :return: builds and return the msg by the protocol
    '''
    msg = port + '&' + file_len
    return create_response('06', msg)

def create_login_response_msg(msg):
    '''

    :param msg:string that describes response to login
    :return:build and return the msg by the protocol
    '''
    return create_response('02', msg)

def create_register_response_msg(msg):
    '''

    :param msg:string that describes response to register
    :return:build and return the msg by the protocol
    '''
    return create_response('03', msg)

def create_upload_file_response_msg(msg):
    '''

    :param msg:string that describes response to upload
    :return:build and return the msg by the protocol
    '''
    return create_response('05', msg)

def create_delete_file_response_msg(msg):
    '''

    :param msg:string that describes response to the delete
    :return:build and return the msg by the protocol
    '''
    return create_response('07', msg)

def create_insert_file_to_folder_response_msg(msg):
    '''

    :param msg:string that describes response to insert the file into folder
    :return:build and return the msg by the protocol
    '''
    return create_response('08', msg)

def create_create_folder_response_msg(msg):
    '''

    :param msg:string that describes response to create folder
    :return:build and return the msg by the protocol
    '''
    return create_response('09', msg)

def create_change_detail_response_msg(msg):
    '''

    :param msg:string that describes response to change details
    :return:build and return the msg by the protocol
    '''
    return create_response('10', msg)

def create_share_file_response_msg(msg):
    '''

    :param msg:string that describes response to share file or folder
    :return:build and return the msg by the protocol
    '''
    return create_response('11', msg)

def create_change_file_name_response_msg(msg):
    '''

    :param msg:string that describes response to change files or folders name
    :return:build and return the msg by the protocol
    '''
    return create_response('13', msg)

def create_response(code, msg):
    '''

    :param code:code of the response by protocol
    :param msg:msg to the client
    :return:create and return response msg by the protocol
    '''

    msg = code + msg
    return msg


if __name__ == '__main__':
    msg = input('enter massage to unpack: ')
    print(unpack_msg(msg))