# -- coding: utf-8 --

from utils import gdal_calc
from osgeo import gdal
import os


def read_geo_file(file_path):
    res = []
    with open(file_path, "r") as f:
        res = f.readlines()
    return res


# 读取 geo 坐标文件，以字典格式返回.包含仿射矩阵和投影
def get_img_geo_info(geo_file_path):
    dtic1 = {}
    geo_data = read_geo_file(geo_file_path)
    for geo in geo_data:
        d = tuple(eval(geo))
        img_name = os.path.split(d[0])[1].split(".")[0]
        dtic1[img_name] = d[1], d[2]
    return dtic1


def get_block_geo_info(block_path):
    res = []
    for tif_img in os.listdir(block_path):
        if tif_img.split(".")[-1] not in ['jpg', 'tif', 'png']:
            continue
        tif_path = os.path.join(block_path, tif_img)
        print(" === get geo info === :", tif_path)
        geo_data = gdal_calc.get_geo_info(tif_path)
        res.append(str(geo_data))
        print(geo_data)
    print(res)
    return res


# 获取 tif 文件坐标，写入txt文件
def block_write_geo_info_to_txt(block_path, file_path, write_type):
    res = get_block_geo_info(block_path)
    # if os.path.exists(file_path):  # 如果文件存在
    #     # 删除文件
    #     os.remove(file_path)
    # 重新编辑
    with open(file_path, write_type) as f:
        f.writelines([line + '\n' for line in res])


def total_geo_info_to_txt(input_path, file_path):
    block_list = os.listdir(input_path)
    for i, block_name in enumerate(block_list):
        if i == 0:
            write_type = 'w'
        else:
            write_type = 'a'
        block_path = os.path.join(input_path, block_name)
        block_write_geo_info_to_txt(block_path, file_path, write_type)


# 把txt文件的坐标信息，写入jpg图片
def block_write_geo_info_to_img(geo_info_path, block_jpg_path):
    # if not os.path.exists(save_block_jpg_path):
    #     os.makedirs(save_block_jpg_path)
    dict1 = get_img_geo_info(geo_info_path)
    for img in os.listdir(block_jpg_path):
        if img.split(".")[-1] not in ['jpg']:
            continue
        img_path = os.path.join(block_jpg_path, img)
        # save_img_path = os.path.join(save_block_jpg_path, img)

        img_name = img.split(".")[0]
        # print(img, img_name, save_img_path)
        # print(dict1[img_name][0])
        # print(dict1[img_name][1])
        dataset = gdal.Open(img_path)

        dataset.SetGeoTransform(dict1[img_name][0])
        dataset.SetProjection(dict1[img_name][1])  # 写入投影
        dataset.FlushCache()
        # # # 保存写入jpg文件
        # driver = gdal.GetDriverByName("JPEG")  # 数据类型必须有，因为要计算需要多大内存空间
        # driver.CreateCopy(save_img_path, dataset)
        #
        del dataset  # 关闭对象，文件dataset


if __name__ == "__main__":
    pass
    block_path = r"F:\YiDuDom3bangs\YiDu1027_DOM"
    total_path = r"F:\YiDuDom_new\jpg"
    geo_info_path = r"F:\YiDuDom_new\geo_info.txt"
    # block_write_geo_info_to_txt(block_path, geo_info_path)
    total_geo_info_to_txt(total_path, geo_info_path)

    # geo_info_path = r"F:\YiDuDom_new\geo_info.txt"
    # block_jpg_path = r"F:\YiDuDom3bangs\YiDu1027_DOM_jpg_cut_save_merge"
    # block_write_geo_info_to_img(geo_info_path, block_jpg_path)

    # block_write_geo_info_to_img(geo_info_path, block_jpg_path, block_jpg_path2)

    # res = read_geo_file(file_path)
    # print(res)
    # print(res[0])
    # print(tuple(eval(res[0]))[1])
    # print(type(tuple(eval(res[0]))[1][0]), tuple(eval(res[0]))[1][0])
    # print(type(tuple(eval(res[0]))[1][1]), tuple(eval(res[0]))[1][1])
    # print(type(tuple(eval(res[0]))[1][2]), tuple(eval(res[0]))[1][2])
    # print((tuple(eval(res[0]))[1][1]) + (tuple(eval(res[0]))[1][0]))
