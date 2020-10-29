# -- coding: utf-8 --

import os
import shutil


def rename_file():
    path = r"F:\songzi_block_shp\szy1"
    for file in os.listdir(path):
        old_name = os.path.join(path, file)
        print(file.split(".")[0].split("_")[1])
        print(file.split(".")[1])
        new_name = os.path.join(path, file.split(".")[0].split("_")[1] + '.' + file.split(".")[1])
        os.rename(old_name, new_name)


def copy_block(block_path, copy_path):
    # block_path = "F:\pos_calculation_YiDu2"
    # copy_path = "F:\pos_calculation_YiDu2"
    for img_name in os.listdir(block_path):
        print('===', img_name, os.path.join(block_path, img_name))
        for _img in os.listdir(os.path.join(block_path, img_name)):
            ori_img = os.path.join(block_path, img_name, _img)
            copy_img = os.path.join(copy_path, img_name + _img)
            if not os.path.exists(copy_path):
                os.makedirs(copy_path)
            print('===', _img, ori_img, copy_img)

            shutil.copyfile(ori_img, copy_img)


def copy_error_img():
    ori_path = r"F:\pos_calculation_YiDu2\block7_jpg_cut_all"
    error_path = r"F:\error"
    error_path2 = r"F:\error2"
    if not os.path.exists(error_path2):
        os.makedirs(error_path2)

    error_list = os.listdir(error_path)
    for error_img in error_list:
        print(error_img)
        ori_img = os.path.join(ori_path, error_img.split(".")[0] + '.png')
        copy_img = os.path.join(error_path2, error_img)
        shutil.copyfile(ori_img, copy_img)


if __name__ == "__main__":
    print("exectue file:", __file__)
    copy_error_img()
    # rename_file()
