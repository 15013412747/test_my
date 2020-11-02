# -- coding: utf-8 --

import os


# from tools import tif_geo_info


def read_geo_file(file_path):
    res = []
    with open(file_path, "r") as f:
        res = f.readlines()
    return res


def get_img_geo_info(geo_file_path):
    dtic1 = {}
    geo_data = read_geo_file(geo_file_path)
    for geo in geo_data:
        d = tuple(eval(geo))
        img_name = os.path.split(d[0])[1].split(".")[0]
        dtic1[img_name] = d[1]
    return dtic1


def get_pos_data(pos_file_path):
    res = []
    with open(pos_file_path, 'r')as f:
        res = f.readlines()
    return res


def calc_pos(csv_path):
    # 图片的经纬度信息
    dict1 = get_img_geo_info(r"G:\SongZi_new3bangs\geo_info.txt")
    pos_list = get_pos_data(r"G:\SongZi_new3bangs\output_res.txt")
    with open(csv_path, "w") as f:
        for sick_tree in pos_list:
            img_path = sick_tree.split("|")[0]
            # 病树画框位置信息
            pos_list = eval(sick_tree.split("|")[1])
            x = (pos_list[0] + pos_list[2]) / 2
            y = (pos_list[1] + pos_list[3]) / 2
            img_info = os.path.split(img_path)
            # img_name 图片名字 字典索引字段
            img_name = os.path.split(img_info[0])[1]
            img_serise = img_info[1]
            # 切割后小图的位置 row  column
            img_size = int(img_serise.split("_")[2])
            row = int(img_serise.split("_")[0])
            col = int(img_serise.split("_")[1])
            print(""
                  ""
                  "")
            print(" === geo info === : ", dict1[img_name])
            print()
            print(" === img info === : img_size", img_size, "row", row, "col", col)
            print(img_path)
            print(pos_list, type(pos_list[0]))
            geo = dict1[img_name]
            # 经度
            longitude = geo[0] + (col * img_size + x) * geo[1]
            # 纬度
            latitude = geo[3] + (row * img_size + y) * geo[5]
            # print(img_name, longitude, latitude)
            str2 = img_name + ',' + str(longitude) + ',' + str(latitude)
            print(str2)
            f.write(str2 + '\n')


if __name__ == "__main__":
    # dict1 = get_img_geo_info(r"G:\SongZi_new3bangs\geo_info.txt")
    # pos_list = get_pos_data(r"G:\SongZi_new3bangs\output_res.txt")
    print("========")
    calc_pos(r"G:\SongZi_new3bangs\sick_tree_pos.csv")
    print("========")

    # print(pos_list)
    # print(dict1['songzi_yang5_20201017_1-0-0'][0],type(dict1['songzi_yang5_20201017_1-0-0'][0]))
    pass
