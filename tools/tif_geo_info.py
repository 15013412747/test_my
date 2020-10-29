# -- coding: utf-8 --

from utils import gdal_calc
import os


def get_block_geo_info(block_path):
    res = []
    for tif_img in os.listdir(block_path):
        tif_path = os.path.join(block_path, tif_img)
        geo_data = gdal_calc.get_geo_info(tif_path)
        res.append(str(geo_data))
        print(geo_data)
    print(res)
    return res


def write_block_geo_info(block_path, file_path):
    res = get_block_geo_info(block_path)
    with open(file_path, "w") as f:
        f.writelines([line + '\n' for line in res])


def read_geo_file(file_path):
    res = []
    with open(file_path, "r") as f:
        res = f.readlines()
    return res


if __name__ == "__main__":
    block_path = r"G:\pos_calculation_YiDu\block7_tif"
    file_path = r"G:\test\test.txt"
    # write_block_geo_info(block_path, file_path)
    res = read_geo_file(file_path)
    print(res)
    print(res[0])
    print(tuple(eval(res[0]))[1])
    print(type(tuple(eval(res[0]))[1][0]), tuple(eval(res[0]))[1][0])
    print(type(tuple(eval(res[0]))[1][1]), tuple(eval(res[0]))[1][1])
    print(type(tuple(eval(res[0]))[1][2]), tuple(eval(res[0]))[1][2])
    print((tuple(eval(res[0]))[1][1]) + (tuple(eval(res[0]))[1][0]))
