import os
import sys
import pathlib
import hashlib
from collections import defaultdict


def check_and_return_directory(argument):
    if len(argument) == 1:
        print("Directory is not specified")
        exit()
    else:
        return argument[1]


def check_and_return_format(file_format):
    if file_format == '':
        return ''
    else:
        return "." + file_format


def keep_on_asking_int(prompt_msg, opt_list, err_msg):
    option = int(input(prompt_msg))
    print()
    while option not in opt_list:
        print(err_msg)
        option = int(input(prompt_msg))
        print()
    return option


def keep_on_asking_y_or_n(prompt_msg, err_msg):
    option = input(prompt_msg)
    print()
    while option not in ["yes", "no"]:
        print(err_msg)
        option = input(prompt_msg)
        print()
    return option


# TASK TWO
def sort_operation(directory, _reverse_order, file_format=''):
    file_dict = walk_and_get_dict(directory, file_format)
    sort_and_print_path(file_dict, _reverse_order)
    return file_dict


# used in sort_operation
def walk_and_get_dict(directory, file_format=''):
    dictionary = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            size = os.path.getsize(path)
            if pathlib.PurePosixPath(path).suffix == file_format:
                dictionary[size].append(path)
            elif file_format == '':
                dictionary[size].append(path)

    return dictionary


# used in sort_operation()
def sort_and_print_path(dictionary, _reverse):
    for key, value in sorted(dictionary.items(), reverse=_reverse):
        print(str(key) + " bytes")
        for _v in value:
            print(_v)
        print()


# TASK THREE
def check_duplicates_operation(dictionary, _reverse_order):
    counter = 0
    dict2 = defaultdict(dict)
    dict3 = defaultdict(dict)
    for size, path in sorted(dictionary.items(), reverse=_reverse_order):
        for x in path:
            with open(x, 'rb') as _f:
                _f_bytes = _f.read()
                _hash = hashlib.md5(_f_bytes).hexdigest()
            if not dict2[size].get(_hash):
                dict2[size][_hash] = []
            dict2[size][_hash].append(x)

    for _size, _dict in dict2.items():
        print(str(_size) + " bytes")
        for _hash, _path in _dict.items():
            if len(_path) > 1:
                print("Hash: " + _hash)
                for _name in _path:
                    counter += 1
                    _newname = str(counter) + ". " + _name
                    print(_newname)
                    # prepare dict3 = {size: {hash: [only duplicated files]}} for remove application
                    if not dict3[_size].get(_hash):
                        dict3[_size][_hash] = []
                    dict3[_size][_hash].append(_newname)
        print()
    return dict3


# TASK FOUR
def check_remove_format(dictionary, prompt_msg, err_msg):
    path_num_list = []
    _all_element_exist = True
    _rem_op_list = input(prompt_msg).split()
    print()

    while _rem_op_list == []:
        print(err_msg)
        _rem_op_list = input(prompt_msg).split()

    for _size, _dict in dictionary.items():
        for _hash, _path in _dict.items():
            for _name in _path:
                path_num_list.append(_name.split(". ", 1)[0])
    for element in _rem_op_list:
        element_exist = True if element in path_num_list else False
        _all_element_exist = _all_element_exist and element_exist

    while not _all_element_exist:
        _all_element_exist = True
        print(err_msg)
        _rem_op_list, _all_element_exist = check_remove_format(dictionary, prompt_msg, err_msg)

    return _rem_op_list, _all_element_exist


def remove_dup_operation(dictionary, rem_option_list):
    _space_freed = 0
    print(dictionary)
    for _size, _dict in dictionary.items():
        for _hash, _path in _dict.items():
            for _name in _path:
                for x in rem_option_list:
                    if _name.split(". ", 1)[0] == x:
                        os.remove(_name.split('. ', 1)[1])
                        # print(f"File '{_name.split('. ', 1)[1]}' with size {_size} removed...")
                        _space_freed += _size
    return _space_freed


# 0 # Manual alternative - uncomment this and comment # 1 #
# cur_dir = check_and_return_directory(["", "D:\\02 WK2-JVM"])

# 1 # Check argument and return if specified, otherwise stop
cur_dir = check_and_return_directory(sys.argv)

# 2 # Prompt input for file format
_format = check_and_return_format(input("Enter file format:\n"))
print()

# 3 # Prompt input for sort option until correct input is given
print("Size sorting options:\n1. Descending\n2. Ascending\n")
sort_option = keep_on_asking_int("Enter a sorting option:\n", [1, 2], "Wrong option\n")
if sort_option == 1:
    reverse_order = True
else:
    reverse_order = False

# 4 # Perform sort operation
dict1 = sort_operation(cur_dir, reverse_order, _format)

# 5 # Prompt input for "check duplicates" option until correct input is given
dup_option = keep_on_asking_y_or_n("Check for duplicates?\n", "Wrong option\n")

# 6 # Perform "check duplicates" operation
if dup_option == "yes":
    dict3 = check_duplicates_operation(dict1, reverse_order)

# 7 # Prompt input for "remove duplicates" option until correct input is given
rem_option = keep_on_asking_y_or_n("Delete files?\n", "Wrong option\n")

# 8 # Perform "remove duplicates" operation
if rem_option == "yes":
    rem_op_list, all_element_exist = check_remove_format(dict3, "Enter file number to delete:\n", "Wrong format\n")
    if all_element_exist:
        space_freed = remove_dup_operation(dict3, rem_op_list)
        print(f"Total freed up space: {space_freed} bytes")
