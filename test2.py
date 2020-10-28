import pingjie
from utils import trans_2_img
import shutil
import os


def copy_block(block_path, copy_path):
    # block_path = "F:\pos_calculation_YiDu2"
    # copy_path = "F:\pos_calculation_YiDu2"
    for img_name in os.listdir(block_path):
        print('===', img_name, os.path.join(block_path, img_name))
        for _img in os.listdir(os.path.join(block_path, img_name)):
            ori_img = os.path.join(block_path, img_name, _img)
            copy_img = os.path.join(copy_path, img_name+_img)
            if not os.path.exists(copy_path):
                os.makedirs(copy_path)
            print('===', _img, ori_img, copy_img)

            shutil.copyfile(ori_img, copy_img)


if __name__ == "__main__":
    #
    # block_path = r"F:\pos_calculation_YiDu2\block7_jpg_cut"
    # copy_path = r"F:\pos_calculation_YiDu2\block7_jpg_cut_all"
    # copy_block(block_path, copy_path)

    block_path = r"F:\pos_calculation_YiDu2\block7_jpg_cut_save"
    copy_path = r"F:\pos_calculation_YiDu2\block7_jpg_cut_save_all"
    copy_block(block_path, copy_path)