import os
import sys


def add_path(path, index=1):
    sys.path.insert(index, path)


def add_sym_link(path, folder_name):
    # Get the current path
    current_path = os.getcwd()
    link_name = os.path.join(current_path, folder_name)
    os.symlink(path, link_name, True)


def remove_sym_link(path):
    # Get the current path
    os.unlink(path)