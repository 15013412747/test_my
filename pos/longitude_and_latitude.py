# -- coding: utf-8 --

from skimage import io, data
import math
import numpy as np

cos30 = math.cos(math.pi / 6)
# 每一经度或者纬度的长度 单位 m
longitude_d = 111 * 1000
latitude_d = 111 * 1000 * cos30
# 无人机经度和纬度位置
longitude = 30.379171
latitude = 114.0571478
# 每个像素大小 单位 m  此变量无人机启动时已经预设 需要配置
pixel = 0.1

img_name = 'C:\\Users\\86150\\Desktop\\0925001\DSC00003.JPG'


def get_longitude_and_latitude(img_name):
    res = []

    img = io.imread(img_name)
    height = img.shape[0]
    width = img.shape[1]
    # 左上角第一个像素
    f1 = longitude - (height / 2) * 0.1 / longitude_d
    f2 = latitude + (width / 2) * 0.1 / latitude_d
    print(height, width)
    print(f1, f2)
    return
    for i in range(width):
        res.append([])
        print(i)
        for j in range(height):
            print(i, j)

            res[i].append([f1 + (i * 0.1) / longitude_d, f2 - (i * 0.1) / latitude_d])
    print(res)
    return res


def get_longitude_and_latitude2(img_name, x, y):
    img = io.imread(img_name)
    height = img.shape[0]
    width = img.shape[1]

    f1 = longitude + (y - (height / 2)) * 0.1 / longitude_d
    f2 = latitude + ((width / 2) - x) * 0.1 / latitude_d
    return [f1, f2]


# res = []
#
# for i in range(5):
#     res.append([])
#     for j in range(5):
#         res[i].append((i, j))
#         print(res)
# print(res)

if __name__ == "__main__":
    print("中心点经度：%s ，中心点纬度：%s" % (longitude, latitude))
    print(get_longitude_and_latitude2(img_name, 0, 0))
    get_longitude_and_latitude(img_name)
    pass
