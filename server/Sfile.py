import os
import sys
import shutil

def get_file_length(path):
    '''

    :param path:path to file
    :return: the length of the file
    '''
    data = open(path, 'r').read()
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
