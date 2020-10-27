import numpy as np
import gdal
import os
import datetime
from osgeo import ogr


def tans_2_img(in_path, out_path):
    in_ds = gdal.Open(in_path)  # 读取要切的原图
    print(in_ds)
    print(in_ds == None)
    print(in_ds is None)
    if in_ds is not None:
        print("open tif file succeed")
    width = in_ds.RasterXSize  # 获取数据宽度
    height = in_ds.RasterYSize  # 获取数据高度
    outbandsize = in_ds.RasterCount  # 获取数据波段数
    im_geotrans = in_ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = in_ds.GetProjection()  # 获取投影信息
    datatype = in_ds.GetRasterBand(1).DataType
    im_data = in_ds.ReadAsArray()  # 获取数据
    print(width, height, outbandsize, datatype)
    print(im_geotrans)
    print(im_proj)

    exit()
    # 读取原图中的波段1
    in_band1 = in_ds.GetRasterBand(1)
    # in_band2 = in_ds.GetRasterBand(2)
    # in_band3 = in_ds.GetRasterBand(3)
    out_band1 = in_band1.ReadAsArray()

    out_band1[out_band1 != 255] = 0

    ori_transform = in_ds.GetGeoTransform()

    # 写入目标文件
    gtif_driver = gdal.GetDriverByName("GTiff")

    file = out_path
    print(os.path.dirname(file))
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))

    out_ds = gtif_driver.Create(file, height, width, 1, datatype)
    # 设置原点坐标
    out_ds.SetGeoTransform(ori_transform)

    # 设置SRS属性（投影信息）
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(out_band1)

    out_ds.FlushCache()
    del out_ds, out_band1


def PolygonizeTheRaster():
    inputfile = r'E:/dataFile/sz2-0-0.tif'
    ds = gdal.Open(inputfile, gdal.GA_ReadOnly)
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()

    width = ds.RasterXSize  # 获取数据宽度
    height = ds.RasterYSize  # 获取数据高度
    outbandsize = ds.RasterCount  # 获取数据波段数
    im_geotrans = ds.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = ds.GetProjection()  # 获取投影信息
    datatype = ds.GetRasterBand(1).DataType
    im_data = ds.ReadAsArray()  # 获取数据
    print(width, height, outbandsize, datatype)
    print(im_geotrans, im_geotrans[1], im_geotrans[5])
    print(im_proj)

    print(type(maskband), maskband)
    dst_filename = r'E:/dataFile/test.shp'
    drv = ogr.GetDriverByName('ESRI Shapefile')
    dst_ds = drv.CreateDataSource(dst_filename)
    srs = None
    dst_layername = 'out'
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    dst_fieldname = 'DN'
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    dst_field = 0
    prog_func = test()
    options = []
    # 参数  输入栅格图像波段\掩码图像波段、矢量化后的矢量图层、需要将DN值写入矢量字段的索引、算法选项、进度条回调函数、进度条参数
    gdal.Polygonize(srcband, maskband, dst_layer, dst_field, options, callback=prog_func)


def test():
    print('callback prog_func')


PolygonizeTheRaster()
exit()

if __name__ == "__main__":
    time1 = datetime.datetime.now()
    print(time1)
    tans_2_img(r"G:\3bangs_qu\peizhuning2\songzi_no2\sz2-0-0.tif", r"F:\png\test3.tif")
    time2 = datetime.datetime.now()
    print(time2)

    # pass
    # nn2 = np.ones((10000, 10000))
    # print(type(nn2), len(nn2), nn2)
    # print(nn2[1][2])
    # re_lu = lambda x: np.where(x == 1, x, 244)
    # # print(re_lu)
    # arrr = re_lu(nn2)
    # print(nn2[1][2])
    # print('=================')
    # A = np.random.rand(500, 500)
    # print(A)
    # A[A > 0.5] = 5
    # print(A)
