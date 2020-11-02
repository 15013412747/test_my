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
    ds = gdal.Open(tif_img_path)
    driver = gdal.GetDriverByName('JPEG')
    dst_ds = driver.CreateCopy(img_path, ds)

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
        # for tif_img in os.listdir(os.path.join(tif_path, block_path)):
        #     # 文件不存在，创建文件夹
        #     if not os.path.exists(os.path.join(png_path, block_path)):
        #         os.makedirs(os.path.join(png_path, block_path))
        #
        #     # if tif_img in ["block10-0-0.tif", "block10-0-1.tif", "block10-0-2.tif"]:
        #     #     continue
        #     # 处理文件格式，只处理 tif 格式
        #     if tif_img.split(".")[-1] != 'tif':
        #         continue
        #     png_img = tif_img.split(".")[0] + '.png'
        #     tif_img_path = os.path.join(tif_path, block_path, tif_img)
        #     png_img_path = os.path.join(png_path, block_path, png_img)
        #     tif_trans_png(tif_img_path, png_img_path)


if __name__ == "__main__":
    tif_path = r"G:\SongZi_new3bangs\tif"
    # png_path = r"E:\3bangs_qu\png"
    png_path = r"G:\SongZi_new3bangs\jpg"
    total_tif_trans_png(tif_path, png_path)

