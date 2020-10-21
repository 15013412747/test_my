# -*- coding: utf-8 -*-
import gdal
import os
import numpy as np
import threading
import datetime
import time


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
    l = []
    thread_num = 100
    for i in range(thread_num):
        p = threading.Thread(target=trans_img, args=(out_band1[i], i))
    for i in range(len(out_band1)):
        p = threading.Thread(target=trans_img, args=(out_band1[i], i))
        # t1.join()
        # p = Thread(target=work)
        l.append(p)
        p.start()
    for p in l:
        p.join()
        # for j in range(len(out_band1[i])):
        #
        #     if out_band1[i][j] != 255:
        #         out_band1[i][j] = 0

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


def trans_img(arr, index):
    for i in range(len(arr)):
        if arr[i] != 255:
            arr[i] = 0


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


def test_run(ttt, i):
    i = 0
    print(" ===start=== ", ttt, i)
    time.sleep(10)
    print(" ===end=== ", ttt, i)

    # i += 1
    # print(ttt, i)
    # time.sleep(10)


if __name__ == "__main__":
    # thread_num = 20
    # l = []
    # for i in range(thread_num):
    #     ttt = "task:" + str(i)
    #     # print(ttt)
    #     p = threading.Thread(target=test_run, args=(ttt, i))
    #     l.append(p)
    #     p.start()
    #     # p.join()
    # for pp in l:
    #     pp.join()
    time1 = datetime.datetime.now()
    print(time1)  # 2019-01-28 11:09:01.529864
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))  # 2019-01-28 11:09:01.529864
    print(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))  # 20190128110901529864

    time.sleep(6)
    time2 = datetime.datetime.now()
    print(type(time2 - time1), time2 - time1)
    print(time.strptime(time2 - time1, '%Y-%m-%d %H:%M:%S.%f'))
    print("\n====== main end ========")
    exit()
    png_path = r"F:\png"
    # png_path = r"E:\3bangs_qu\png"
    img_2_path = r"F:\two"
    print ("24小时格式：" + time.strftime("%H:%M:%S"))
    # total_tans_2_img(png_path, img_2_path)
    tans_2_img(r"F:\png\szy1-0-0.png", r"F:\png\test.tif")

    print ("24小时格式：" + time.strftime("%H:%M:%S"))
