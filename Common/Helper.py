
def index_helper(str_list, target_str):
    for (index, tmp) in enumerate(str_list):
        if tmp == target_str:
            return index
    return -1

def write_dict_to_file(dict_val, save_file_path):
    sorted_keys = sorted(dict_val.keys())
    with open(save_file_path, 'w') as f:
        for key in sorted_keys:
            f.write(key + ":")
            for val in dict_val[key]:
                try:
                    f.write("%.4lf" % val + '|')
                except:
                    for tmp in val:
                        f.write("%.4lf" % val + '|')
                    f.write('\n')
            f.write('\n')