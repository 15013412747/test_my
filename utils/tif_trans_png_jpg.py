from osgeo import gdal
import os

"""转换图片格式"""


def old_function():
    base_path = "D:/3bands/q1_2/"
    with open(os.path.join(os.path.join(base_path, '1.txt')), "r") as f:
        lines = f.read().splitlines()
    for ii, line in enumerate(lines):
        file_path = os.path.join(base_path, 'tif/', str(line) + ".tif")
        ds = gdal.Open(file_path)
        driver = gdal.GetDriverByName('PNG')
        savepath = os.path.join(base_path, 'png/', str(line) + ".png")
        print(line)
        dst_ds = driver.CreateCopy(savepath, ds)
        dst_ds = None
        src_ds = None


def tif_trans_png(tif_img_path, png_img_path):
    print("=== start transfer: ", tif_img_path, png_img_path)
    ds = gdal.Open(tif_img_path)
    driver = gdal.GetDriverByName('PNG')
    dst_ds = driver.CreateCopy(png_img_path, ds)
    print("=== end transfer: ", tif_img_path, png_img_path)


def tif_trans_jpg(tif_img_path, img_path):
    print("=== start transfer: ", tif_img_path, img_path)
    in_ds = gdal.Open(tif_img_path)
    print(in_ds.RasterCount)
    width = in_ds.RasterXSize  # 获取数据宽度
    height = in_ds.RasterYSize  # 获取数据高度
    outbandsize = in_ds.RasterCount  # 获取数据波段数
    im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()  # 获取投影信息
    datatype = in_ds.GetRasterBand(1).DataType

    mem = gdal.GetDriverByName("MEM")
    out_ds = mem.Create("", width, height, 3, datatype)

    # 设置裁剪出来图的原点坐标
    out_ds.SetGeoTransform(im_geotrans)
    # 设置SRS属性（投影信息）
    out_ds.SetProjection(im_proj)

    # 读取原图中的每个波段
    in_band1 = in_ds.GetRasterBand(1)
    in_band2 = in_ds.GetRasterBand(2)
    in_band3 = in_ds.GetRasterBand(3)

    out_band1 = in_band1.ReadAsArray()
    out_band2 = in_band2.ReadAsArray()
    out_band3 = in_band3.ReadAsArray()

    out_ds.GetRasterBand(1).WriteArray(out_band1)
    out_ds.GetRasterBand(2).WriteArray(out_band2)
    out_ds.GetRasterBand(3).WriteArray(out_band3)

    driver = gdal.GetDriverByName('JPEG')
    dst_ds = driver.CreateCopy(img_path, out_ds)

    print("=== end transfer: ", tif_img_path, img_path)


# tif_trans_jpg(r"G:\pos_calculation_YiDu\block7_tif\block7-0-0.tif", r"G:\test\test.jpg")
# exit()


def block_tif_trans_img(block_path, block_path2, img_type="jpg"):
    print("=== block_tif_trans_img ===", block_path, block_path2)
    if not os.path.exists(os.path.join(block_path2, block_path2)):
        os.makedirs(os.path.join(block_path2, block_path2))
    for tif_img in os.listdir(block_path):
        print("=== tif_img === :", tif_img)
        tif_path = os.path.join(block_path, tif_img)

        img_name = tif_img.split(".")[0] + '.jpg'
        if img_type == "png":
            img_name = tif_img.split(".")[0] + '.png'
        img_path = os.path.join(block_path2, img_name)
        if not os.path.exists(block_path2):
            os.makedirs(block_path2)
        tif_trans_jpg(tif_path, img_path)


# block_tif_trans(r"G:\SongZi_Zhengti\songzi_yang5_20201017_zhengti_3band",
#                 r"G:\SongZi_Zhengti\songzi_yang5_20201017_zhengti_jpg")
# exit()


def total_tif_trans_png(tif_path, png_path):
    print(tif_path, png_path)
    if not os.path.exists(png_path):
        os.makedirs(png_path)
    tif_path_list = os.listdir(tif_path)
    print("tif path", tif_path_list)
    for block_name in tif_path_list:
        # """ block_path1 为被转换的 tif 格式区块路径"""
        block_path1 = os.path.join(tif_path, block_name)
        # """ block_path2 被转换后的 jpg或者png 格式区块路径"""
        block_path2 = os.path.join(png_path, block_name)
        block_tif_trans_img(block_path1, block_path2)


if __name__ == "__main__":
    pass
    # tif_path = r"G:\SongZi_new3bangs\tif"
    # png_path = r"G:\SongZi_new3bangs\jpg"
    # total_tif_trans_png(tif_path, png_path)
    tif_trans_jpg(r"F:\YiDuDom\block7\block7-0-0.tif", r"F:\YiDuDom\block7_jpg\block7-0-0.jpg")
