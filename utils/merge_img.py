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


# 定义图像拼接函数 单张图片拼接
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
                                str(IMAGE_SIZE) + '_' + str(IMAGE_SIZE) + '.jpg')
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


# 拼接一个目录下的所有小图片为一张大图 拼单张图片
# 根据图片命名来自动计算行列数
#
def image_compose2(file_name, img_save_path):
    # 遍历所有图片
    img_list = os.listdir(file_name)
    img_total = len(img_list)
    # print(img_total, img_list)
    img_column = 0
    for _img in img_list:
        if _img[0] == '0':
            img_column = img_column + 1
        else:
            break
        # print(_img[0], _img)
    img_row = int(img_total / img_column)

    print(img_total, img_column, img_row)

    to_image = Image.new('RGB', (img_column * IMAGE_SIZE, img_row * IMAGE_SIZE))  # 创建一个新图
    # to_image = Image.new('L', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    num = 0
    mnu = 0
    for y in range(0, img_row):
        for x in range(0, img_column):

            # path = file_name + str(num) + '_' + str(mnu) + '_' + \
            #        str(IMAGE_SIZE) + '_' + str(IMAGE_SIZE) + '.png'
            path = os.path.join(file_name, str(num) + '_' + str(mnu) + '_' + \
                                str(IMAGE_SIZE) + '_' + str(IMAGE_SIZE) + '.jpg')

            from_image = Image.open(path).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 0) * IMAGE_SIZE, (y - 0) * IMAGE_SIZE))
            mnu += 1
            if mnu == img_column:
                mnu = 0
                num += 1

    return to_image.save(img_save_path)  # 保存新图


# 拼接一个目录下的所有小图片为一张大图 拼单张图片
# 根据图片大小调整拼接
def image_compose3(img_name, img_save_path):
    # 遍历所有图片
    img_list = os.listdir(img_name)
    img_total = len(img_list)
    # print(img_total, img_list)
    img_column = 0
    len_y = 0
    len_x = 0
    # 横向计算图片总长度
    for _img in img_list:
        info_img_list = _img.split('_')
        if info_img_list[0] == '0':
            img_column = img_column + 1
            len_x = len_x + int(info_img_list[3].split('.')[0])
        else:
            break

    # 纵向计算图片总长度
    for _img in img_list:
        info_img_list = _img.split('_')
        if info_img_list[1] == '1':
            len_y = len_y + int(info_img_list[2])
        else:
            continue
        # print(_img[0], _img)
    img_row = int(img_total / img_column)

    print(img_total, img_column, img_row, len_x, len_y)

    to_image = Image.new('RGB', (len_x, len_y))  # 创建一个新图

    for _img in img_list:
        path = os.path.join(img_name, _img)
        info_img_list = _img.split('_')
        print(info_img_list)
        y = int(info_img_list[0])
        x = int(info_img_list[1])
        IMAGE_SIZE_y = int(info_img_list[2])
        IMAGE_SIZE_x = int(info_img_list[3].split('.')[0])

        # print(IMAGE_SIZE_x, IMAGE_SIZE_y)

        from_image = Image.open(path).resize(
            (IMAGE_SIZE_x, IMAGE_SIZE_y), Image.ANTIALIAS)
        to_image.paste(from_image, ((x - 0) * IMAGE_SIZE, (y - 0) * IMAGE_SIZE))
        # to_image.paste(from_image, ((x - 0) * IMAGE_SIZE_y, (y - 0) * IMAGE_SIZE_x))

    to_image.save(img_save_path)  # 保存新图


# 拼接所有区块
def total_merge_img(in_path, out_path):
    in_path_list = os.listdir(in_path)
    for block_name in in_path_list:
        if block_name not in ["block8"]:
            continue
        # print(q_dir)
        block_path = os.path.join(in_path, block_name)
        out_path2 = os.path.join(out_path, block_name)
        block_merge(block_path, out_path2)
        # print(os.listdir(os.path.join(in_path, q_dir)))
        # # block_merge(cut_img_path, merge_img_path)
        # for img_name in os.listdir(os.path.join(in_path, q_dir)):
        #     print("=== img_name:", img_name)
        #     cut_img_path = os.path.join(os.path.join(in_path, q_dir, img_name))
        #     merge_img_path = os.path.join(os.path.join(out_path, q_dir))
        #     if not os.path.exists(merge_img_path):
        #         os.makedirs(merge_img_path)
        #     print("cut", cut_img_path)
        #     # print(merge_img_path)
        #     merge_img2(cut_img_path, merge_img_path)


def block_merge(block_path, merge_block_path):
    if not os.path.exists(merge_block_path):
        os.makedirs(merge_block_path)

    for img_name in os.listdir(block_path):
        print(os.path.join(block_path, img_name))
        path1 = os.path.join(block_path, img_name)
        path2 = os.path.join(merge_block_path, img_name) + '.jpg'
        print(path1, path2)
        image_compose3(path1, path2)


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
    in_path = r"F:\YiDuDom_jpg\cut_save2"
    out_path = r"F:\YiDuDom_jpg\merge_img"
    total_merge_img(in_path, out_path)
    # block_merge(r"G:\YiDuDom_new\cut_save", r"G:\YiDuDom_new\cut_save_merge")
    # in_path = r"G:\pos_calculation_YiDu2"
    # out_path = r"G:\pos_calculation_YiDu3\block7_jpg_mem"
    # total_merge_img(in_path, out_path)
