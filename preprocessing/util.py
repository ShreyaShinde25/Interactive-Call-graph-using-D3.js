
def sort_dict(d: dict, reverse=True):
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=reverse))