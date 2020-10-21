import PIL.Image as Image
import os
# noinspection PyUnresolvedReferences
from pathlib import Path

# IMAGES_PATH = '/Users/liuhongyan/xiangmu/data/merge/crop/'  #小文件夹 图片集地址
IMAGES_FORMAT = ['.jpg', '.png']  # 图片格式

# src = input('请输入图片文件路径：')
IMAGE_SIZE = 1000  # 每张小图片的大小
IMAGE_ROW = 30  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 30  # 图片间隔，也就是合并成一张图后，一共有几列


# 定义图像拼接函数
def image_compose(file_name, IMAGE_SAVE_PATH):
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # to_image = Image.new('L', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    num = 0
    mnu = 0
    for y in range(0, IMAGE_ROW):
        for x in range(0, IMAGE_COLUMN):

            # path = file_name + str(num) + '_' + str(mnu) + '_' + \
            #        str(IMAGE_SIZE) + '_' + str(IMAGE_SIZE) + '.png'
            path = os.path.join(file_name, str(num) + '_' + str(mnu) + '_' + \
                                str(IMAGE_SIZE) + '_' + str(IMAGE_SIZE) + '.png')
            # print(path)
            # f_dir_name = os.path.split(os.path.split(os.path.split(path)[0])[0])[1]

            from_image = Image.open(path).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 0) * IMAGE_SIZE, (y - 0) * IMAGE_SIZE))
            mnu += 1
            if mnu == IMAGE_COLUMN:
                mnu = 0
                num += 1

    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


def total_merge_img(in_path, out_path):
    in_path_list = os.listdir(in_path)
    for q_dir in in_path_list:
        # print(q_dir)
        print(os.listdir(os.path.join(in_path, q_dir)))
        for img_name in os.listdir(os.path.join(in_path, q_dir)):
            print("=== img_name:", img_name)
            cut_img_path = os.path.join(os.path.join(in_path, q_dir, img_name))
            merge_img_path = os.path.join(os.path.join(out_path, q_dir))
            if not os.path.exists(merge_img_path):
                os.makedirs(merge_img_path)
            print("cut", cut_img_path)
            # print(merge_img_path)
            merge_img2(cut_img_path, merge_img_path)


def merge_img2(cut_img_path, merge_img_path):
    file_name = os.path.join(cut_img_path)

    image_names = [name for name in os.listdir(file_name) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]
    save_path = os.path.join(merge_img_path, os.path.split(file_name)[1] + '.png')
    print(file_name, save_path)
    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")
    print("== imgs: ", file_name)
    print("== save: ", save_path)
    image_compose(file_name, save_path)  # 调用函数


# src = input('请输入图片文件路径：')  # 路径的上一层
# dstpath = input('请输入图片输出目录（不输入路径则表示使用源图片所在目录）：')

def merge_img(cut_img_path, merge_img_path):
    # cut_img_path = ""
    # merge_img_path = ""
    list = os.listdir(cut_img_path)
    print(list)

    for i, sample in enumerate(list):
        if sample != '.DS_S' and sample != '.DS_Store':
            # file_name = cut_img_path + str(sample) + '/'

            file_name = os.path.join(cut_img_path)
            print("== imgs: ", file_name)

            # save_path = merge_img_path + str(sample) + '.png'

            # 合并后的图片路径
            save_path = os.path.join(merge_img_path, os.path.split(file_name)[1] + '.png')
            IMAGE_SAVE_PATH = save_path  # 图片转换后的地址

            # f_dir_name = os.path.split(os.path.split(os.path.split(path)[0])[0])[1]
            # list = os.listdir(src)
            # 获取图片集地址下的所有图片名称
            image_names = [name for name in os.listdir(file_name) for item in IMAGES_FORMAT if
                           os.path.splitext(name)[1] == item]

            # 简单的对于参数的设定和实际图片集的大小进行数量判断
            if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
                raise ValueError("合成图片的参数和要求的数量不能匹配！")
            print("== save: ", IMAGE_SAVE_PATH)
            image_compose(file_name, IMAGE_SAVE_PATH)  # 调用函数
        else:
            continue


if "__main__" == __name__:
    in_path = r"F:\3bangs_qu\save_img"
    out_path = r"F:\3bangs_qu\merge_img"
    total_merge_img(in_path, out_path)
