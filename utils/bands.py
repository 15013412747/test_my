import gdal
import os

"""转换图片波段"""


def read_img(pos_img_name):
    # 第一步 读取文件
    dataset = gdal.Open(pos_img_name)  # 打开文件
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数

    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息

    return pos_img_name, im_geotrans, im_proj


# 转换 tif 文件波段
def band4_to_band3(band4_path, band3_path):
    print(" === start band4 trans to band3")
    in_ds = gdal.Open(band4_path)  # 读取要切的原图
    print("open tif file succeed")
    width = in_ds.RasterXSize  # 获取数据宽度
    height = in_ds.RasterYSize  # 获取数据高度
    outbandsize = in_ds.RasterCount  # 获取数据波段数
    im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()  # 获取投影信息
    datatype = in_ds.GetRasterBand(1).DataType
    im_data = in_ds.ReadAsArray()  # 获取数据
    print(width, height, outbandsize, datatype)
    # 去读坐标信息
    # ori_transform 数据结构：
    # (111.586453936076, 5.753036668243302e-07, 0.0, 30.208775394866, 0.0, -4.998577917582736e-07)
    ori_transform = in_ds.GetGeoTransform()

    # 读取原图中的每个波段
    in_band1 = in_ds.GetRasterBand(1)
    in_band2 = in_ds.GetRasterBand(2)
    in_band3 = in_ds.GetRasterBand(3)

    out_band1 = in_band1.ReadAsArray()
    out_band2 = in_band2.ReadAsArray()
    out_band3 = in_band3.ReadAsArray()

    # 写入目标文件
    gtif_driver = gdal.GetDriverByName("GTiff")

    # file = r'E:\test\test2.tif'

    file = band3_path
    # 创建文件夹路径
    file_dir = os.path.dirname(file)
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    out_ds = gtif_driver.Create(file, height, width, 3, datatype)

    # 设置裁剪出来图的原点坐标
    out_ds.SetGeoTransform(ori_transform)

    # 设置SRS属性（投影信息）
    out_ds.SetProjection(in_ds.GetProjection())

    out_ds.GetRasterBand(1).WriteArray(out_band1)
    out_ds.GetRasterBand(2).WriteArray(out_band2)
    out_ds.GetRasterBand(3).WriteArray(out_band3)
    out_ds.FlushCache()

    del out_ds, out_band1, out_band2, out_band3  # out_band4
    print(" === end band4 trans to band3")
    return band4_path, im_geotrans, im_proj


def block_band4_to_band3(block_path, block_path2):
    for tif_img in os.listdir(block_path):
        print(tif_img)

        # 文件不存在，创建文件夹
        if not os.path.exists(os.path.join(block_path2)):
            os.makedirs(os.path.join(block_path2))
        # 非 tif 不做处理，只处理 tif 格式文件
        if tif_img.split(".")[-1] != 'tif':
            continue
        band4_path = os.path.join(block_path, tif_img)
        band3_path = os.path.join(block_path2, tif_img)
        print(band4_path, band3_path)
        band4_to_band3(band4_path, band3_path)


# block_band4_to_band3(r"G:\SongZi_Zhengti\songzi_yang5_20201017_zhengti",
#                      r"G:\SongZi_Zhengti\songzi_yang5_20201017_zhengti_3band")
# exit()


# 转换所有 tif 文件波段
def total_band4_to_band3(ori_path, new_path):
    # ori_path = r"E:\qu"
    # new_path = r"E:\3bangs_qu\tif"

    tif_path_list = os.listdir(ori_path)
    # 遍历区块
    for block_dir in tif_path_list:
        # 只转设定区块的数据
        # if not block_dir in ["YiDu1027_DOM"]:
        #     continue
        # 遍历区块下的文件夹
        block_path = os.path.join(ori_path, block_dir)
        block_path2 = os.path.join(new_path, block_dir)
        block_band4_to_band3(block_path, block_path2)
        # for tif_img in os.listdir(os.path.join(ori_path, block_dir)):
        #     print(tif_img)
        #
        #     # 文件不存在，创建文件夹
        #     if not os.path.exists(os.path.join(new_path, block_dir)):
        #         os.makedirs(os.path.join(new_path, block_dir))
        #     # 非 tif 不做处理，只处理 tif 格式文件
        #     if tif_img.split(".")[-1] != 'tif':
        #         continue
        #     band4_path = os.path.join(ori_path, block_dir, tif_img)
        #     band3_path = os.path.join(new_path, block_dir, tif_img)
        #     print(band4_path, band3_path)
        #     band4_to_band3(band4_path, band3_path)


if __name__ == "__main__":
    # print("switch bands start ===")
    # path1 = r'G:\SongZi_new'
    # path2 = path1 + '3bangs'
    # print(path1, path2)
    # total_band4_to_band3(path1, path2)
    pass
    # band4_to_band3(r'G:\pos_calculation_YiDu\block7_tif\block7-0-0.tif', r'G:\YiDuDom2\block7\block7-0-0.tif')
    # band4_to_band3(r'E:\qu\songzi_yang4\szy4-0-0.tif', r'E:\3bangs_qu\tif\szy2-3-2.tif')
    # band4_to_band3(r'E:\qu\songzi_yang2\szy2-4-1.tif', r'E:\3bangs_qu\tif\szy2-4-1.tif')
