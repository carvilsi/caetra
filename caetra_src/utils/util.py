import sys
import os

def get_shield_config_path(path):

    print(os.path.realpath(path))
    return os.path.splitext(os.path.realpath(path))[0] + ".tmol"
    
