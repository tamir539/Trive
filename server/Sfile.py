import os
import shutil
from Encryption import AESCipher
from settings import TRIVE_LOCATION as trive_path

def get_file_length(path):
    '''

    :param path:path to file
    :return: the length of the file
    '''
    data = open(path, 'rb').read()
    return len(data)


def create_folder(path):
    '''

    :param path:path to create folder in
    :return: creates the folder
    '''
    try:
        os.makedirs(path)
        return 'ok'
    except:
        return 'no'


def rename_file(path, new_name):
    '''

    :param path:path to file or folder
    :param new_name: new name of the file\folder
    :return: rename the file\folder
    '''
    path_with_no_name = path[:path.rindex('\\')]
    try:
        os.rename(path, path_with_no_name + '\\' + new_name)
        return 'ok'
    except Exception as e:
        print('in rename file: ',str(e))
        return 'no'


def delete_file(path, username):
    '''

    :param path:path to file or folder
    :return:delete the file or folder
    '''
    if os.path.isfile(path):
        if 'recycle' not in path:
            move_file(path, f'{trive_path}\\{username}\\recycle')
        os.remove(path)
        return 'ok'
    elif os.path.isdir(path):
        if 'recycle' not in path:
            move_file(path, f'{trive_path}\\{username}\\recycle')
        shutil.rmtree(path)
        return 'ok'
    return 'no'


def share_file(trive_path, path, username):
    '''

    :param trive_path:path of trive
    :param path: path of the file or folder to share
    :param username: username to share with
    :return: move the file\ folder to the username shared folder
    '''

    if os.path.isdir(path):
        folder_name = path[path.rindex('\\') + 1:]
        try:
            shutil.copytree(path, trive_path + '\\' + username + '\\shared\\' + folder_name, copy_function = shutil.copy)
            return 'ok'
        except Exception as e:
            print('in share file ', str(e))
            return 'no'
    else:
        try:
            shutil.copy2(path, trive_path + '\\' + username + '\\shared' )
            return 'ok'
        except:
            return 'no'


def move_file(path, move_to):
    '''

    :param path:path of the fie or folder
    :param move_to: path to move the file or folder to
    :return: move the file or folder to the new path
    '''
    if os.path.isdir(path):
        folder_name = path[path.rindex('\\') + 1:]
        try:
            shutil.copytree(path, move_to + '\\' + folder_name, copy_function = shutil.copy)
            return 'ok'
        except Exception as e:
            print('in move file file ', str(e))
            return 'no'
    else:
        try:
            shutil.copy2(path, move_to)
            return 'ok'
        except Exception as e:
            print('in move file file ', str(e))
            return 'no'


def encrypt_file(path, key):
    '''

    :param path:path to file to encrypt
    :param key: aes key to encrypt with
    :return:
    '''

    out_file_path = 'D:\\Trive\\enc_file'

    file_data = bytearray()

    with open(path, 'rb') as in_file:
        data = in_file.read()
        file_len = len(data)

    while len(file_data) < file_len:
        size = file_len - len(file_data)
        try:
            if size >= 1024:
                file_data.extend(key.encrypt(size))
                data = data[:1024]
            else:
                if size != 0:
                    file_data.extend(key.encrypt(size))
                break
        except Exception as e:
            print(f'in encrypt file - {str(e)}')
            file_data = None
            break
    if file_data:
        with open(out_file_path, 'wb') as out_file:
            out_file.write(file_data)


