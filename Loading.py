"""
Module of Shtonda Yelizaveta, contains functions for data loading
"""
import Information
import Builder
import json


def load_ini(path):
    """
    :param path: relative path to .ini file
    opens .ini file, processes  and prints 'OK' if there are no errors
    :return: list of keys from .ini file
    """
    with open(path, 'r', encoding='utf8') as f:
        r = json.load(f)
        check_ini_file(r)
        main_file = r['input']['csv']
        additional_file = r['input']['json']
        input_encoding = r['input']['encoding']
        output_file = r['output']['fname']
        output_encoding = r['output']['encoding']
        print('OK')
        return [main_file, additional_file, input_encoding, output_file, output_encoding]


def check_ini_file(r):
    """
    :param r: dictionary, loaded from .ini file
    checks existence of needed keys and raises error if some key is absent
    :return: True if there are no errors
    """
    input_keys = ['csv', 'json', 'encoding']
    output_keys = ['fname', 'encoding']
    input_list = []
    output_list = []
    for i in r['input']:
        input_list.append(i)
    for i in r['output']:
        output_list.append(i)
    if not input_list >= input_keys:
        raise ValueError('Something wrong with input keys in .ini file')
    if not output_list >= output_keys:
        raise ValueError('Something wrong with output keys in .ini file')
    return True


def load(main_file, addition_file, input_encoding):
    """
    :param main_file: relative path to .csv file
    :param addition_file: relative path to .json file
    :param input_encoding: type of encoding of main_file and addition_file
    creates instance of the class Information, calls functions for loading main_file and addition_file, checks
    their accordance and prints appropriate text
    :return: instance of the class Information
    """
    data = Information.Information()
    load_data(data, main_file, input_encoding)
    if fit(data, load_stat(addition_file, input_encoding)):
        print('OK')
    else:
        print('UPS')
    return data


def load_data(data, main_file, input_encoding):
    """
    :param data: object of class Information
    :param main_file: relative path to .csv file
    :param input_encoding: type of encoding of main_file
    clears data, creates instance of the class Builder, pass parameters to Builder method and prints 'OK'
    if there are no errors
    """
    print(f'input-csv {main_file}: ', end='')
    data.clear()
    obj = Builder.Builder()
    obj.load(data, main_file, input_encoding)
    print('OK')


def load_stat(additional_file, input_encoding):
    """
    :param additional_file: relative path to .json file
    :param input_encoding: type of encoding of additional_file
    opens additional file, checks existence of needed keys and raises error if some key is absent
    :return: dictionary loaded from additional_file
    """
    print(f'input-json {additional_file}: ', end='')
    keys = ["сума довжин всіх прізвищ", "кількість записів"]
    with open(additional_file, 'r', encoding=input_encoding) as f:
        add_data = json.load(f)
        for key in keys:
            if key not in add_data:
                raise ValueError('There are no needed keys in additional file')
        add_data["surnames_sum"] = add_data.pop("сума довжин всіх прізвищ")
        add_data["records_sum"] = add_data.pop("кількість записів")
    print('OK')
    return add_data


def fit(data, add_data):
    """
    :param data: object of class Information
    :param add_data: dictionary loaded from additional_file, returned in load_stat() function
    checks accordance of data from additional_file to corresponding data in lst
    :return: True if data is according, False otherwise
    """
    print('json?=csv: ', end='')
    record_sum = data.records_sum
    surname_sum = data.surnames_length
    return surname_sum == add_data["surnames_sum"] and record_sum == add_data["records_sum"]


