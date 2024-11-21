import os


def create_dir(DIR):
    if not os.path.exists(DIR):
        os.mkdir(DIR)
