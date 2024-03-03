import os
import shutil
import time

from config import BASE_DATA_PATH, BASE_PATH


def create_directory_structure(path, strct=None, replace=False):

    if strct is None:
        strct = {}
    if not strct:
        return None

    dir_files = os.listdir(path)
    for name, v in strct.items():
        if name in dir_files and isinstance(v, dict):
            if replace:
                shutil.rmtree(f"{path}/{name}")
                os.mkdir(f"{path}/{name}")
            create_directory_structure(path=f"{path}/{name}", strct=v)
        else:
            if isinstance(v, dict):
                os.mkdir(f"{path}/{name}")
                create_directory_structure(path=f"{path}/{name}", strct=v)
            elif isinstance(v, str):
                with open(os.path.join(path, name), 'w+') as fp:
                    fp.write(v)


if __name__ == '__main__':

    structure = {
        "root_4": {
            "Subdir3": {
                "hello.py": "hello world",
                "bye.py": "byebye"
            }
        }
    }
    create_directory_structure(path=f"{BASE_DATA_PATH}/root_3",
                               strct=structure, replace=True)