import cv2
import math
import os
# noinspection PyUnresolvedReferences
import numpy as np
from PIL import Image
from pathlib import Path

Image.MAX_IMAGE_PIXELS = None
IMAGES_FORMAT = ['.png']  # 图片格式


# 切图方法 切割单张图片为 1000 * 1000 大小的散图
# ori_img_path  源图片路径
# save_img_path  保存图片路径
# img_name  图片名字
def cut_image(ori_img_path, save_img_path, img_name):
    file_name = os.path.join(ori_img_path, str(img_name))
    # save_path = dstpath + str(sample[:-4]) + '/'
    save_path = os.path.join(save_img_path, str(img_name[:-4]))
    # save_path = os.path.join(save_img_path)
    print("from", file_name, "to", save_path)
    Path(save_path).mkdir(parents=True, exist_ok=True)
    # block size
    height = 1000
    width = 1000

    # overlap
    over_x = 0
    over_y = 0
    h_val = height - over_x
    w_val = width - over_y

    # Set whether to discard an image that does not meet the size
    mandatory = False
    print(str(file_name))
    img = cv2.imread(file_name)

    # print(img.shape)
    # original image size
    original_height = img.shape[0]
    original_width = img.shape[1]

    # max_row = float((original_height - height) / h_val)  # + 1
    # max_col = float((original_width - width) / w_val)  # + 1
    max_row = float(original_height / h_val)  # + 1
    max_col = float(original_width / w_val)  # + 1

    # block number
    max_row = math.ceil(max_row) if mandatory == False else math.floor(max_row)
    max_col = math.ceil(max_col) if mandatory == False else math.floor(max_col)

    # print(max_row)
    # print(max_col)

    images = []
    # 图片格式
    img_type = ".jpg"

    for i in range(max_row):
        images_temp = []
        for j in range(max_col):
            # temp_path = save_path + '/' + str(img_name.split(".")[0]) + str(i) + '_' + str(j) + '_'
            temp_path = save_path + '/' + str(i) + '_' + str(j) + '_'
            if ((width + j * w_val) > original_width and (
                    i * h_val + height) <= original_height):  # Judge the right most incomplete part
                temp = img[i * h_val:i * h_val + height, j * w_val:original_width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + img_type
                # temp = temp[:, :, 0]
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            elif ((height + i * h_val) > original_height and (
                    j * w_val + width) <= original_width):  # Judge the incomplete part at the bottom
                temp = img[i * h_val:original_height, j * w_val:j * w_val + width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + img_type
                # temp = temp[:, :, 0]
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            elif ((width + j * w_val) > original_width and (
                    i * h_val + height) > original_height):  # Judge the last slide
                temp = img[i * h_val:original_height, j * w_val:original_width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + img_type
                # temp = temp[:, :, 0]
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)
            else:
                temp = img[i * h_val:i * h_val + height, j * w_val:j * w_val + width, :]
                temp_path = temp_path + str(temp.shape[0]) + '_' + str(temp.shape[1]) + img_type
                # temp = temp[:, :, 0]
                cv2.imwrite(temp_path, temp)
                images_temp.append(temp)  # The rest of the complete

        images.append(images_temp)


# 切割文件下所有图片 目前所有图片都是二级结构
# root        入口目录
#   - block1  区块目录
#     - img1  区块中图片
#     - img2
def total_cut_image(input_img_path, output_img_path):
    input_img_path_list = os.listdir(input_img_path)
    # 遍历区块
    for block_name in input_img_path_list:
        print("=== block_name === :", block_name)
        # img_list = os.listdir(os.path.join(input_img_path, q_dir))
        # cut_image(input_img_path, output_img_path, q_dir)
        block_path1 = os.path.join(input_img_path, block_name)
        block_path2 = os.path.join(output_img_path, block_name)
        block_cut_img(block_path1, block_path2)


# 对一个区块的所有图片进行切割
def block_cut_img(block_path, cut_path):
    img_list = os.listdir(block_path)
    # 遍历图片
    for img_name in img_list:
        # 不是图片不处理
        print("=== img_name === :", img_name, img_name.split(".")[-1].lower(),
              img_name.split(".")[-1].lower() not in ['jpg', 'png'])
        if img_name.split(".")[-1].lower() not in ['jpg', 'png']:
            continue
        cut_image(block_path, cut_path, img_name)


# block_path = r"F:\YiDuDom3bangs\YiDu1027_DOM_jpg"
# cut_path = r"F:\YiDuDom3bangs\YiDu1027_DOM_jpg_cut"
# block_cut_img(block_path, cut_path)
# exit()

# 跳跃的切割原始图片为训练集
def cut_block_img_tran(block_path, cut_path):
    img_list = os.listdir(block_path)
    # 遍历图片
    i = 0
    for _img in img_list:
        i += 1
        print(i)
        if i % 4 != 0:
            continue

        # 不是图片不处理
        print("===============")
        print(i, _img, _img.split(".")[-1].lower(), _img.split(".")[-1].lower() not in ['jpg', 'png'])
        if _img.split(".")[-1].lower() not in ['jpg', 'png']:
            continue
        cut_image(block_path, cut_path, _img)


# cut_block_img_tran(r"F:\20201028_YiDu\1", r"F:\20201028_YiDu\tran")
# cut_block_img_tran(r"F:\20201028_YiDu\2", r"F:\20201028_YiDu\tran")
# exit()


if "__main__" == __name__:
    pass
    # 切割一个区块
    # block_path = r"G:\pos_calculation_YiDu\block7_jpg"
    # block_cut_path = r"G:\pos_calculation_YiDu\block7_jpg_cut"
    # block_cut_img(block_path, block_cut_path)

    # 切割所有
    path1 = r"F:\YiDuDom_jpg\jpg"
    path2 = r"F:\YiDuDom_jpg\jpg_cut"
    total_cut_image(path1, path2)

    # _cut_image(r"G:\pos_calculation_YiDu\block7_jpg", r"G:\pos_calculation_YiDu\block7_jpg_cut", "DSC00304.JPG")
