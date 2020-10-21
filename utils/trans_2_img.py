# -*- coding: utf-8 -*-
import gdal
import os
import numpy as np


# 转二制图
def tans_2_img(in_path, out_path):
    file = out_path
    print(os.path.dirname(file))
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    in_ds = gdal.Open(in_path)  # 读取要切的原图
    print("open tif file succeed")
    width = in_ds.RasterXSize  # 获取数据宽度
    height = in_ds.RasterYSize  # 获取数据高度
    outbandsize = in_ds.RasterCount  # 获取数据波段数
    im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()  # 获取投影信息
    datatype = in_ds.GetRasterBand(1).DataType
    im_data = in_ds.ReadAsArray()  # 获取数据
    print(width, height, outbandsize, datatype)

    # 读取原图中的波段1
    in_band1 = in_ds.GetRasterBand(1)
    # in_band2 = in_ds.GetRasterBand(2)
    # in_band3 = in_ds.GetRasterBand(3)
    out_band1 = in_band1.ReadAsArray()
    # 提取红框部分
    out_band1[out_band1 != 255] = 0

    ori_transform = in_ds.GetGeoTransform()

    # 写入目标文件
    gtif_driver = gdal.GetDriverByName("GTiff")

    out_ds = gtif_driver.Create(file, height, width, 1, datatype)
    # 设置原点坐标
    out_ds.SetGeoTransform(ori_transform)

    # 设置SRS属性（投影信息）
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(out_band1)

    out_ds.FlushCache()
    del out_ds, out_band1


def total_tans_2_img(png_path, img_2_path):
    tif_path_list = os.listdir(png_path)
    for q_dir in tif_path_list:
        for img_name in os.listdir(os.path.join(png_path, q_dir)):
            if "sz1-0-0.png" == img_name:
                continue
            # 文件不存在，创建文件夹
            if not os.path.exists(os.path.join(png_path, q_dir)):
                os.makedirs(os.path.join(png_path, q_dir))

            # if tif_img in ["block10-0-0.tif", "block10-0-1.tif", "block10-0-2.tif"]:
            #     continue
            # 处理文件格式，只处理 png 格式
            if img_name.split(".")[-1] != 'png':
                continue
            png_img = img_name.split(".")[0] + '.png'
            png_img_path = os.path.join(png_path, q_dir, img_name)
            two_img_path = os.path.join(img_2_path, q_dir, img_name.split(".")[0] + '.tif')
            print(png_img_path, two_img_path)
            tans_2_img(png_img_path, two_img_path)
            # exit()


if __name__ == "__main__":
    png_path = r"F:\3bangs_qu\merge_img"
    # png_path = r"E:\3bangs_qu\png"
    img_2_path = r"F:\3bangs_qu\two"
    total_tans_2_img(png_path, img_2_path)
