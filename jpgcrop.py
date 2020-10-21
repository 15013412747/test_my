import numpy as np
import matplotlib
import os
from PIL import Image

def img_seg(dir):
    files = os.listdir(dir)
    id = 1
    for file in files:
        a, b = os.path.splitext(file)
        img = Image.open(os.path.join(dir + "\\" + file))
        hight, width = img.size
        w = 512
        i = 0
        while (i + w <= hight):
            j = 0
            while (j + w <= width):
                new_img = img.crop((i, j, i + w, j + w))
                # rename = "D:\\labelme\\images\\"
                rename = "E:/bb/"
                new_img.save(rename + a + "_" + str(id) + b,dpi=(72.0,72,0))
                id += 1
                j += w
            i = i + w


if __name__ == '__main__':
    # path = "D:\\labelme\\data\\images\\train"
    path = "E:/bad"
    img_seg(path)