import os
import numpy as np
import json


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


def create_probability_space(critical_probability):
    prob_array = np.arange(0.05, 0.5, 0.05)
    critical_values = np.arange(0.5, 0.7, 0.005)
    critical_values = np.insert(critical_values, -1, critical_probability)
    critical_values.sort()
    prob_array = np.concatenate((prob_array, critical_values))
    end_values = np.arange(0.7, 1, 0.05)
    prob_array = np.concatenate((prob_array, end_values))
    return prob_array


def save_json_file(dict_with_data, json_file_name, sub_dir=''):
    path = os.path.join(sub_dir, json_file_name) if sub_dir else json_file_name
    json_file = open(path, 'w')
    json.dump(dict_with_data, json_file)
    json_file.close()
    print(f'Created new file {json_file_name} with simulation data.')


def read_json_file(json_file_name, sub_dir=''):
    path = os.path.join(sub_dir, json_file_name) if sub_dir else json_file_name
    print(f'Reading data from file {json_file_name}...')
    json_file = open(path, 'r')
    dict_with_data = json_file.read()
    dict_with_data = json.loads(dict_with_data)
    json_file.close()
    return dict_with_data


def ask_to_replace_file(file_name):
    print(f'File with name {file_name} already exists. '
          f'Do you want to perform new simulation? [y/n]')
    while True:
        answer = input()
        if answer == 'y':
            return True
        elif answer == 'n':
            return False
        else:
            print('Please type "y" for yes or "n" for no.')
