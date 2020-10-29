import os

from utils import bands
from utils import tif_png2
from utils import cut_img
from config.properties import Properties

# 图像转波段
# 图像转png
# 图像切割

# 读取配置信息
pro = Properties('config/config.proerties')
properties = pro.get_properties()

print("config info:")
print(properties)

input_path = properties['input_path']
output_path = properties['output_path']

input_path = r"F:\YiDuDom"
output_path = r"F:\YiDuDom2\block7"

if __name__ == "__main__":
    # 转波段
    # band3_path = os.path.join(output_path, '3bang_tif_path')
    band3_path = os.path.join(input_path)
    print(band3_path)
    bands.total_band4_to_band3(input_path, output_path)

    # tif 转化 png
    png_path = os.path.join(output_path, 'png_path')
    tif_png2.total_tif_trans_png(band3_path, png_path)

    # png 切图
    cut_path = os.path.join(output_path, 'cut_path')
    cut_img.cut_image_total(png_path, cut_path)
