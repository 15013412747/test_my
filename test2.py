import pingjie
from utils import trans_2_img

if __name__ == "__main__":
    # 转波段
    in_path = r"F:\3bangs_qu\save_img"
    out_path = r"F:\3bangs_qu\merge_img"
    pingjie.total_merge_img(in_path, out_path)

    png_path = r"F:\3bangs_qu\merge_img"
    # png_path = r"E:\3bangs_qu\png"
    img_2_path = r"F:\3bangs_qu\two"
    trans_2_img.total_tans_2_img(png_path, img_2_path)
