# -- coding: utf-8 --
import os
import shutil


def read_sick_tree_file(sick_tree_file):
    res = []
    with open(sick_tree_file) as f:
        res = f.readlines()
    return res


# 挑出病树红框数据图片
# sick_tree_file   病树数据文件
# dector_path      被拷贝目录
# tran_path        拷贝目录
def get_sick_tree_img(sick_tree_file, dector_path, tran_path):
    if not os.path.exists(tran_path):
        os.makedirs(tran_path)
    res = read_sick_tree_file(sick_tree_file)
    for sick_info in res:
        img_path = sick_info.split("|")[0]
        img_name_list = img_path.split("/")
        img_path2 = img_path[img_path.index("cut_save") + len("cut_save") + 1:]
        img_path2 = os.sep.join(img_path2.split('/'))[:-1]

        sick_tree_img_path = os.path.join(dector_path, img_path2)
        tran_img_path = os.path.join(tran_path, img_name_list[-2] + '_tran_' + img_name_list[-1])
        print(sick_tree_img_path, tran_img_path)
        shutil.copy(sick_tree_img_path, tran_img_path)


if __name__ == "__main__":
    sick_tree_file = r"G:\YiDuDom_new\output_res.txt"
    dector_path = r"G:\YiDuDom_new\cut_save"
    tran_path = r"G:\YiDuDom_new\tran"
    get_sick_tree_img(sick_tree_file, dector_path, tran_path)
