def get_file_length(path):
    '''

    :param path:path to file
    :return: the length of the file
    '''
    data = open(path, 'r').read()
    return len(data)