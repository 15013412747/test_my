from osgeo import gdal
import os


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


def block_tif_trans(block_path, block_path2, img_type="jpg"):
    if not os.path.exists(block_path2):
        os.makedirs(block_path2)
    for tif_img in os.listdir(block_path):
        print(tif_img)
        tif_path = os.path.join(block_path, tif_img)

        img_name = tif_img.split(".")[0] + '.jpg'
        if img_type == "png":
            img_name = tif_img.split(".")[0] + '.png'
        img_path = os.path.join(block_path2, img_name)

        tif_trans_jpg(tif_path, img_path)


# block_tif_trans(r"F:\YiDuDom3bangs\YiDu1027_DOM", r"F:\YiDuDom3bangs\YiDu1027_DOM_jpg")
# exit()


def total_tif_trans_png(tif_path, png_path):
    print(tif_path, png_path)
    # tif_path = "E:\\3bangs_qu\\tif"
    # tif_path = r"D:\YiDuDOM3bangs"
    # png_path = r"E:\3bangs_qu\png"
    # png_path = r"E:\sick_tree_sample\png"

    # if not os.path.exists(png_path):
    #     os.

    tif_path_list = os.listdir(tif_path)
    print("tif path", tif_path_list)
    for q_dir in tif_path_list:
        for tif_img in os.listdir(os.path.join(tif_path, q_dir)):
            # 文件不存在，创建文件夹
            if not os.path.exists(os.path.join(png_path, q_dir)):
                os.makedirs(os.path.join(png_path, q_dir))

            # if tif_img in ["block10-0-0.tif", "block10-0-1.tif", "block10-0-2.tif"]:
            #     continue
            # 处理文件格式，只处理 tif 格式
            if tif_img.split(".")[-1] != 'tif':
                continue
            png_img = tif_img.split(".")[0] + '.png'
            tif_img_path = os.path.join(tif_path, q_dir, tif_img)
            png_img_path = os.path.join(png_path, q_dir, png_img)
            tif_trans_png(tif_img_path, png_img_path)


if __name__ == "__main__":
    tif_path = r"F:\YiDuDOM2"
    # png_path = r"E:\3bangs_qu\png"
    png_path = r"F:\YiDuDOM2\png"
    total_tif_trans_png(tif_path, png_path)
