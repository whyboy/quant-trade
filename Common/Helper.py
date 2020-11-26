
def index_helper(str_list, target_str):
    for (index, tmp) in enumerate(str_list):
        if tmp == target_str:
            return index
    return -1
