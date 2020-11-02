# -- coding: utf-8 --

from skimage import io, data
import math, ast
import numpy as np
import json
import os

cos30 = math.cos(math.pi / 6)
# 1 经度长度
longitude_d = 111 * 1000
# 1 纬度长度
latitude_d = 111 * 1000 * cos30

# 一个像素点大小 10cm * 10cm
map_piexls_size = 0.1
# 切割图片大小 [ height, width ]
pic_size = [1000, 1000]
# 图片切割数量 [ y * x ]
pic_num = [6, 8]
# 图片pos字典数据集合
every_pos_dic = {}
# 去掉冗余的病树集合
sick_tree_redundancy = []


def test4():
    file_path = "C:\\Users\\86150\\Desktop\\output_6_softnms.json"
    with open(file_path, encoding='utf-8') as f:
        res = f.readlines()
        print(type(res[0]))
        print((res[0]))
        print("======", res[0].split(','))
        res_list = res[0].split(',')
        print(res_list[0])


def img_center_pos():
    pos_file_path = "C:\\Users\\86150\\Desktop\\pos.csv"
    res = []
    dic = {}
    with open(pos_file_path, encoding='utf-8-sig') as f:
        # print(f.readline())
        for ele in f.readlines():
            ele_list = ele.split(",")
            # print(ele.split(","))
            res.append((ele_list[0].split('.')[0], [ele_list[1], ele_list[2]]))
        dic = dict(res)
    return dic


def read_file():
    file_path = "C:\\Users\\86150\\Desktop\\output_6_softnms.json"
    csv_path = "C:\\Users\\86150\\Desktop\\result.csv"
    redundancy_csv_path = "C:\\Users\\86150\\Desktop\\result2.csv"

    json_data = ""
    with open(file_path) as f:
        # json_data = json.load(f)
        json_data = f.readlines()
    # if not os.path.isdir(csv_path):
    #     os.mkdir(csv_path)
    print(json_data)
    # return
    with open(csv_path, "w") as f2:
        for item in json_data:
            # print(item['name'], item['bbox'], [30.1768642, 111.4301916])
            # sick_tree_info = sick_tree_pos(item['name'], item['bbox'])
            item_list = item.split("|")
            name = item_list[0].split("/")[-1]
            box = ast.literal_eval(item_list[1].strip())
            sick_tree_info = sick_tree_pos(name, box)
            if (not is_redundancy_tree(sick_tree_info)):
                sick_tree_redundancy.append(sick_tree_info)
            f2.write(",".join(sick_tree_info) + '\n')
    print("=== === ", sick_tree_redundancy)
    print("=== === ", len(sick_tree_redundancy))
    res_info = ""
    with open(redundancy_csv_path, "w") as f3:
        for e in sick_tree_redundancy:
            res_info = res_info + e[0] + ',' + e[1] + ',' + e[2] + '\n'
        f3.write(res_info)
        # f3.writelines(sick_tree_redundancy)


# sick_tree_pos(res_list[0].split("/")[-1], res_list[1].split(","), [30.1768642, 111.4301916], [6, 8], [884, 994])


def is_redundancy_tree(tree_info):
    for tree1 in sick_tree_redundancy:
        # print(distance_tree(tree_info[1], tree_info[2], tree1[1], tree1[2]))
        if (distance_tree(tree_info[1], tree_info[2], tree1[1], tree1[2]) < 10):
            print(tree_info)
            print(tree1)
            return True
    return False


def sick_tree_pos(pic_name, sick_tree_pos):
    pic_name2 = pic_name[:pic_name.index(".")]
    # print(pic_name2)

    name_list = pic_name2.split("_")

    # print("sick_tree_pos", sick_tree_pos)
    x = round((float(sick_tree_pos[1]) + float(sick_tree_pos[3])) / 2)
    y = round((float(sick_tree_pos[0]) + float(sick_tree_pos[2])) / 2)

    longitude = float(every_pos_dic[name_list[0]][1])
    latitude = float(every_pos_dic[name_list[0]][0])
    # print("=== :" + name_list[0], longitude, latitude)
    height = pic_num[0] * pic_size[0]
    width = pic_num[1] * pic_size[1]

    # print("name_list", name_list)

    f1 = longitude + (y + int(name_list[1]) * int(name_list[3]) - (width / 2)) * 0.1 / longitude_d
    f2 = latitude + ((height / 2) - (x + int(name_list[2]) * int(name_list[4]))) * 0.1 / latitude_d
    # print(pic_name, f1, f2)
    return [pic_name, str(f1), str(f2)]


def distance_tree(longitude1, latitude1, longitude2, latitude2):
    """传入经纬度，计算两个点的距离"""
    y = abs(float(longitude1) - float(longitude2)) * longitude_d
    x = abs(float(latitude1) - float(latitude2)) * latitude_d
    # print(x, y)
    return math.sqrt(x * x + y * y)


if __name__ == "__main__":
    every_pos_dic = img_center_pos()
    # print(every_pos_dic[])
    read_file()
    # a = distance_tree(30.1739858919749, 111.431245054954, 30.1738329721738, 111.430676586486)
    # b = distance_tree(30.1750698541019, 111.432183793693, 30.1752955928558, 111.431943253153)
    # print(a)
    # print(b)
