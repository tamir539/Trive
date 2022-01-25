import os


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