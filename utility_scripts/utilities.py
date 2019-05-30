from os import path


def findpaths(current_file):
    '''
    input: __file__ (generaly)
    outputs: file_path  abs path of __file__ which called function 
             current_dir, abs dir path of __file__ which called function
             parent_dir, abs dir path of parent dir to current dir
    '''
    file_path = path.abspath(current_file)
    current_dir = path.dirname(file_path)
    parent_dir = path.dirname(current_dir)
    return file_path, current_dir, parent_dir

# print(file_path, parent_dir)
