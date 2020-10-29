from osgeo import gdal
import os
import numpy as np
import cv2

'''
input:原图的tif文件和预测的单通道png图像
out:合成新的tif,带有坐标信息
'''


class GRID:

    # 读图像文件
    def read_img(self, filename):
        dataset = gdal.Open(filename)  # 打开文件

        im_width = dataset.RasterXSize  # 栅格矩阵的列数
        im_height = dataset.RasterYSize  # 栅格矩阵的行数

        im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
        im_proj = dataset.GetProjection()  # 地图投影信息
        im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵

        del dataset  # 关闭对象，文件dataset
        return im_proj, im_geotrans, im_data, im_width, im_height

    # 写文件，以写成tif为例
    def write_img(self, filename, im_proj, im_geotrans, im_data):
        print('111')

        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

        # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape
        print('222')

        # 创建文件
        driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
        print('333', im_bands, im_bands == 1)

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                print(i)
                dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
        print('444')

        del dataset


def get_geo_info(pos_img_name):
    # 第一步 读取文件
    dataset = gdal.Open(pos_img_name)  # 打开文件

    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息

    return pos_img_name, im_geotrans, im_proj


# 提取tif文件经纬度信息 和 jpg图片 像素信息 生成一个带经纬度的JPG图片
# pos_img_name 带坐标的tif格式图片
# data_img_name jpg图片
# new_img 新生成的图片
def write_geo_info_to(pos_img_name, data_img_name, new_img):
    new_img_path = os.path.dirname(new_img)
    if not os.path.exists(new_img_path):
        os.makedirs(new_img_path)
    # 第一步 读取文件
    dataset = gdal.Open(pos_img_name)  # 打开文件

    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息

    # 像素文件
    dataset2 = gdal.Open(data_img_name)  # 打开文件
    im_data2 = dataset2.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵
    dataset2.SetGeoTransform(im_geotrans)
    dataset2.SetProjection(im_proj)  # 写入投影
    driver = gdal.GetDriverByName("JPEG")  # 数据类型必须有，因为要计算需要多大内存空间
    # 第三步 保存写入jpg文件
    driver.CreateCopy(new_img, dataset2)

    del dataset, dataset2  # 关闭对象，文件dataset


# write_geo_info_to(r"G:\pos_calculation_YiDu\block7_tif\block7-0-0.tif", r"G:\YiDuDom2\cut_save_merge\block7-0-0.jpg",
#                   r"G:\YiDuDom2\cut_save_merge2\block7-0-0.jpg")
#
# exit()


def read_img2(filename):
    dataset = gdal.Open(filename)  # 打开文件

    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵
    print(im_width, im_height)
    print("仿射矩阵:  ", im_geotrans)
    print("地图投影信息:  ", im_proj)
    print("地图投影信息:  ", type(im_proj), im_proj is None)
    print("im_data:  ", im_data.shape)
    print("im_data:  ", im_data.dtype.name)


# read_img2(r"G:\YiDuDom2\cut_save_merge2\block7-0-1.jpg")
# exit()

if __name__ == "__main__":
    os.chdir(r'D:/test1')  # 切换路径到待处理图像所在文件夹
    run = GRID()
    # 第一步
    proj, geotrans, data1, row1, column1 = run.read_img('1-0-0.tif')  # 读数据,获取tif图像的信息

    # print(proj, geotrans, data1, row1, column1)
    img_path = '1-0-0.png'  # 读取png图像数据
    data2 = cv2.imread(img_path, -1)

    data = np.array((data2), dtype=data1.dtype)  # 数据格式

    run.write_img('aresult1.tif', proj, geotrans, data)  # 生成tif
