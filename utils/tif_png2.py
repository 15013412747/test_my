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


def total_tif_trans_png(tif_path, png_path):
    # tif_path = "E:\\3bangs_qu\\tif"
    # tif_path = r"D:\YiDuDOM3bangs"
    # png_path = r"E:\3bangs_qu\png"
    # png_path = r"E:\sick_tree_sample\png"

    # if not os.path.exists(png_path):
    #     os.

    tif_path_list = os.listdir(tif_path)
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


def tif_trans_png(tif_img_path, png_img_path):
    print("=== start transfer: ", tif_img_path, png_img_path)
    ds = gdal.Open(tif_img_path)
    driver = gdal.GetDriverByName('PNG')
    dst_ds = driver.CreateCopy(png_img_path, ds)
    print("=== end transfer: ", tif_img_path, png_img_path)


if __name__ == "__main__":
    tif_path = r"D:\YiDuDOM3bangs"
    # png_path = r"E:\3bangs_qu\png"
    png_path = r"E:\sick_tree_sample\png"
    total_tif_trans_png(tif_path, png_path)
