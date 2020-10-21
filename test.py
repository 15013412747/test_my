# -*- coding: utf-8 -*-
import gdal
import numpy as np

in_ds = gdal.Open(r'D:\pin\q7\block7-0-0.png')  # 读取要切的原图
print("open tif file succeed")
width = in_ds.RasterXSize  # 获取数据宽度
height = in_ds.RasterYSize  # 获取数据高度
outbandsize = in_ds.RasterCount  # 获取数据波段数
im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
im_proj = in_ds.GetProjection()  # 获取投影信息
datatype = in_ds.GetRasterBand(1).DataType
im_data = in_ds.ReadAsArray()  # 获取数据
print(width, height, outbandsize, datatype)

# 读取原图中的每个波段
in_band1 = in_ds.GetRasterBand(1)
# in_band2 = in_ds.GetRasterBand(2)
# in_band3 = in_ds.GetRasterBand(3)
print(in_band1)

print("==========")
out_band1 = in_band1.ReadAsArray()
x = 10000
y = 5000
print(x, y, " === ", out_band1[x][y])

out_band1[x][y] = 255
print(type(out_band1), len(out_band1), out_band1[0])
print(type(out_band1), len(out_band1), len(out_band1[0]))

# print(out_band1)

for i in range(len(out_band1)):
    for j in range(len(out_band1[i])):
        if out_band1[i][j] != 255:
            out_band1[i][j] = 0
            # print(i, j)

print('10000 === ', out_band1[10000][10000])

# out_band2 = in_band2.ReadAsArray()
# out_band3 = in_band3.ReadAsArray()

ori_transform = in_ds.GetGeoTransform()

print(ori_transform)
# 写入目标文件
gtif_driver = gdal.GetDriverByName("GTiff")
file = r'F:\test\test2.tif'

out_ds = gtif_driver.Create(file, height, width, 1, datatype)

# 设置裁剪出来图的原点坐标
out_ds.SetGeoTransform(ori_transform)

# 设置SRS属性（投影信息）
out_ds.SetProjection(in_ds.GetProjection())

out_ds.GetRasterBand(1).WriteArray(out_band1)
# out_ds.GetRasterBand(2).WriteArray(out_band2)
# out_ds.GetRasterBand(3).WriteArray(out_band3)

out_ds.FlushCache()

# in_band4 = in_ds.GetRasterBand(4)
exit()

# 定义切图的起始点坐标
offset_x = 0
offset_y = 0

# 定义切图的大小（矩形框）
size = 512
col_num = int(width / size)  # 宽度可以分成几块
row_num = int(height / size)  # 高度可以分成几块
if (width % size != 0):
    col_num += 1
if (height % size != 0):
    row_num += 1
# 这边就知道我们一共是分成了多少个 如果说有多余的 那我们就让那些也自己一小块好吧
num = 1  # 这个就用来记录一共有多少块的
# 现在我们知道的是宽度是1304  高度是666
print("row_num:%d   col_num:%d" % (row_num, col_num))
for i in range(row_num):  # 从高度下手！！！ 可以分成几块！
    for j in range(col_num):
        offset_x = i * size
        offset_y = j * size
        ## 从每个波段中切需要的矩形框内的数据(注意读取的矩形框不能超过原图大小)
        b_ysize = min(width - offset_y, size)
        b_xsize = min(height - offset_x, size)

        print("width:%d     height:%d    offset_x:%d    offset_y:%d     b_xsize:%d     b_ysize:%d" % (
            width, height, offset_x, offset_y, b_xsize, b_ysize))
        # print("\n")
        out_band1 = in_band1.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
        out_band2 = in_band2.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
        out_band3 = in_band3.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
        # out_band4 = in_band4.ReadAsArray(offset_y, offset_x, b_ysize, b_xsize)
        # 获取Tif的驱动，为创建切出来的图文件做准备
        gtif_driver = gdal.GetDriverByName("GTiff")
        file = r'E:/训练文件/newcrop/%04d.jpg' % num
        num += 1
        # 创建切出来的要存的文件
        out_ds = gtif_driver.Create(file, b_ysize, b_xsize, outbandsize, datatype)
        print("create new tif file succeed")

        # 获取原图的原点坐标信息
        ori_transform = in_ds.GetGeoTransform()
        if ori_transform:
            print(ori_transform)
            print("Origin = ({}, {})".format(ori_transform[0], ori_transform[3]))
            print("Pixel Size = ({}, {})".format(ori_transform[1], ori_transform[5]))

        # 读取原图仿射变换参数值
        top_left_x = ori_transform[0]  # 左上角x坐标
        w_e_pixel_resolution = ori_transform[1]  # 东西方向像素分辨率
        top_left_y = ori_transform[3]  # 左上角y坐标
        n_s_pixel_resolution = ori_transform[5]  # 南北方向像素分辨率

        # 根据反射变换参数计算新图的原点坐标
        top_left_x = top_left_x + offset_x * w_e_pixel_resolution
        top_left_y = top_left_y + offset_y * n_s_pixel_resolution

        # 将计算后的值组装为一个元组，以方便设置
        dst_transform = (top_left_x, ori_transform[1], ori_transform[2], top_left_y, ori_transform[4], ori_transform[5])

        # 设置裁剪出来图的原点坐标
        out_ds.SetGeoTransform(dst_transform)

        # 设置SRS属性（投影信息）
        out_ds.SetProjection(in_ds.GetProjection())

        # 写入目标文件
        out_ds.GetRasterBand(1).WriteArray(out_band1)
        out_ds.GetRasterBand(2).WriteArray(out_band2)
        out_ds.GetRasterBand(3).WriteArray(out_band3)
        # out_ds.GetRasterBand(4).WriteArray(out_band4)
        # 将缓存写入磁盘
        out_ds.FlushCache()
        print("FlushCache succeed")
        del out_ds, out_band1, out_band2, out_band3  # out_band4
