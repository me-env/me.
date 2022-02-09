import os
import json
from me.logger import info

# PARSING
import time


def read_line(file):
    f = open(file, 'r')
    lines = f.readlines()
    for line in lines:
        yield line


def fread_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
    return data


def fwrite_json_dict(json_data, file):
    with open(file, 'w') as outfile:
        json.dump(json_data, outfile)


def fwrite_json_string(json_string, file):
    with open(file, 'w') as outfile:
        outfile.write(json_string)


# UTILS

class dct(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# SERVER INTERACTION


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# PERFORMANCES RELATED


def timed(fct):
    def wrap(*args, **kwargs):
        start = time.perf_counter()
        rv = fct(*args, **kwargs)
        end = time.perf_counter()
        info(f"function '{fct.__name__}' took {end - start} to run.")
        return rv

    return wrap


