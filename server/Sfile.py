import os
import shutil

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


def delete_file(path):
    '''

    :param path:path to file or folder
    :return:delete the file or folder
    '''
    if os.path.isfile(path):
        os.remove(path)
        return 'ok'
    elif os.path.isdir(path):
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
        except:
            return 'no'


def encrypt_file(path, key):
    '''

    :param path:path to file to encrypt
    :param key: aes key to encrypt with
    :return:
    '''


    with open(path, 'rb') as in_file:
        with open(out_file_path, 'wb') as out_file:
            # Write salt if present
            if self._salt is not None:
                out_file.write(self._salt)

            # Write filesize of original
            out_file.write(struct.pack('L', filesize))

            # Encrypt to eof
            eof = False
            while not eof:
                in_data = in_file.read(16)
                if len(in_data) == 0:
                    eof = True
                else:
                    out_data = aes_cbc_256.encrypt_block(bytearray(in_data))
                    out_file.write(self.fix_bytes(out_data))



share_file('D:\Trive', 'D:\Trive\\tamir\\aaa.txt', 'try1')