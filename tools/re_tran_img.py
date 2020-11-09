# -- coding: utf-8 --
import os
import shutil


# 读取文件
def read_sick_tree_file(sick_tree_file1):
    res = []
    with open(sick_tree_file1) as f:
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


# 根据病树图片 找出原图
def get_sick_tree_ori_img(ori_path, bad_img_path, re_tran_path):
    if not os.path.exists(re_tran_path):
        os.makedirs(re_tran_path)

    for img_name in os.listdir(bad_img_path):
        img_name_list = img_name.split('_tran_')
        path1 = os.path.join(ori_path, img_name_list[0], img_name_list[1])
        path2 = os.path.join(re_tran_path, img_name)
        print('111', path1)
        print('222', path2)
        shutil.copy(path1, path2)


if __name__ == "__main__":
    pass
    # 选出病树图片
    # sick_tree_file = r"H:\Yidu_new\output_res.txt"
    # dector_path = r"H:\Yidu_new\cut_save"
    # tran_path = r"H:\Yidu_new\tran"
    # get_sick_tree_img(sick_tree_file, dector_path, tran_path)

    # 选出错误原图
    bad_img_path = r"H:\Yidu_new\bad_tran"
    ori_path = r"H:\Yidu_new\cut"
    re_tran_path = r"H:\Yidu_new\re_tran"
    get_sick_tree_ori_img(ori_path, bad_img_path, re_tran_path)
