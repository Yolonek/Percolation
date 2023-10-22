import os


def check_if_file_is_empty(file_path):
    return os.stat(file_path).st_size == 0


def check_if_file_exists(file_path):
    return os.path.exists(file_path)


def check_if_file_has_data(file_path, sub_dir=''):
    path = os.path.join(sub_dir, file_path) if sub_dir else file_path
    if check_if_file_exists(path):
        if check_if_file_is_empty(path) is False:
            return True
        else:
            raise FileNotFoundError
    else:
        return False


def make_directories(list_of_dirs):
    for directory in list_of_dirs:
        if not check_if_file_exists(directory):
            os.mkdir(directory)
