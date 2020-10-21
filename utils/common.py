import os


# 根据文件预设路径，创建文件夹
def mkdir1(path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
