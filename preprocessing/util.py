import os

def mkdir(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)

def get_file_name(path):
    return path.split('/')[-1].split('.')[0]

def sort_dict(d: dict, reverse=True):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

