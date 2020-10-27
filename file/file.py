# -- coding: utf-8 --

import os


def rename_file():
    path = r"F:\songzi_block_shp\szy1"
    for file in os.listdir(path):
        old_name = os.path.join(path, file)
        print(file.split(".")[0].split("_")[1])
        print(file.split(".")[1])
        new_name = os.path.join(path, file.split(".")[0].split("_")[1] + '.' + file.split(".")[1])
        os.rename(old_name, new_name)


if __name__ == "__main__":
    print("exectue file:", __file__)
    # rename_file()
