from osgeo import gdal
import os

base_path="D:/q1/"
ii = '1'
file_path=os.path.join(base_path,str(ii)+".tif")
print(file_path)
ds=gdal.Open(file_path)
driver=gdal.GetDriverByName('PNG')
savepath = os.path.join(base_path,str(ii)+".png")
dst_ds = driver.CreateCopy(savepath, ds)
dst_ds = None
src_ds = None