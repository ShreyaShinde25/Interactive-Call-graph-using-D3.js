import os

def mkdir(dir):
    if os.path.isdir(dir) == False:
        os.mkdir(dir)

def get_file_name(path):
    return path.split('/')[-1].split('.')[0]

def sort_dict(d: dict, reverse=True):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))

def distrib_by_upper_bounds(data, upper_bounds):
    bucket_map = {f"<={k}":0 for k in upper_bounds}
    for k in data:
        for upper in upper_bounds:
            if data[k] <= upper:
                bucket_map[f"<={upper}"] += 1
    return bucket_map