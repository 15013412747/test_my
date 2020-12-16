# -- coding: utf-8 --

from osgeo import gdal, ogr, gdalconst
import time


def world2Pixel(padfTransform, x, y):
    pixel = padfTransform[0] + x * padfTransform[1] + y * padfTransform[2]
    line = padfTransform[3] + x * padfTransform[4] + y * padfTransform[5]
    return (pixel, line)


def get_shp_info():
    driver = ogr.GetDriverByName("ESRI Shapefile")
    dataSource = driver.Open(r"C:\Users\86150\Desktop\data2\test\test.shp")
    print(dataSource)
    layer = dataSource.GetLayer(0)

    print('=====', layer)
    print('=====', dataSource.GetLayerByIndex(0))

    print(layer.GetExtent())

    minX, maxX, minY, maxY = layer.GetExtent()
    print("原边界(坐标系度)：", minX, maxX, maxY, minY)
    # geoTrans = dataset.GetGeoTransform()
    # ulX, ulY = world2Pixel(geoTrans, minX, maxY)
    # lrX, lrY = world2Pixel(geoTrans, maxX, minY)
    # print("新边界：(坐标系米)", ulX, ulY, lrX, lrY)

    shpFile = r"C:\Users\86150\Desktop\data2\test\test.shp"
    shp = ogr.Open(shpFile, 0)
    m_layer = shp.GetLayerByIndex(0)

    print('=====', m_layer)
    print('=====', m_layer.GetExtent())


def test():
    p = r"G:\柑橘影像\NH49D004007.ige"
    pass


def trans_shp_grid():
    # rasterFile = r'G:\柑橘影像\1-0-0.jpg'  # 原影像
    rasterFile = r'G:\柑橘影像\NH49D004007.img'  # 原影像
    shpFile = r"C:\Users\86150\Desktop\data\res.shp"  # 裁剪矩形

    dataset = gdal.Open(rasterFile, gdalconst.GA_ReadOnly)

    geo_transform = dataset.GetGeoTransform()
    cols = dataset.RasterXSize  # 列数
    rows = dataset.RasterYSize  # 行数

    x_min = geo_transform[0]
    y_min = geo_transform[3]
    pixel_width = geo_transform[1]

    shp = ogr.Open(shpFile, 0)
    m_layer = shp.GetLayerByIndex(0)

    layer = shp.GetLayer(0)

    minX, maxX, minY, maxY = layer.GetExtent()
    print("原边界(坐标系度)：", minX, maxX, maxY, minY)

    target_ds = gdal.GetDriverByName('GTiff').Create(r"G:\柑橘影像\res10.tif", xsize=cols, ysize=rows, bands=1,
                                                     eType=gdal.GDT_Byte)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(dataset.GetProjection())

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(-999)
    band.FlushCache()

    print(time.strftime("%Y %m %d %H:%M:%S ", time.localtime()))

    # gdal.RasterizeLayer(target_ds, [1], m_layer, options=["ATTRIBUTE=Shape_Area"])  # 跟shp字段给栅格像元赋值
    gdal.RasterizeLayer(target_ds, [1], m_layer)  # 跟shp字段给栅格像元赋值
    print(time.strftime("%Y %m %d %H:%M:%S ", time.localtime()))

    # gdal.RasterizeLayer(target_ds, [1], m_layer) # 多边形内像元值的全是255
    del dataset
    del target_ds
    shp.Release()


if "__main__" == __name__:
    trans_shp_grid()

    # get_shp_info()
