# import cv2
# import numpy as np
# img = cv2.imread('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM.tif')
# print(np.array(img).max)
# # res = cv2.resize(img, dsize=(1197, 991), interpolation=cv2.INTER_LINEAR)
# # cv2.imwrite('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_resized.tif', res)


# https://stackoverflow.com/questions/41264154/resampling-of-2d-numpy-array
import scipy
from scipy import ndimage, signal
import numpy

# factor = 2

# a = numpy.arange(16).reshape((4,4))
# b = numpy.zeros((a.shape[0]*factor, a.shape[0]*factor))

# print(a.shape)
# print(a)

# b[::factor,::factor] = a
# print(b.shape)
# print(b)
# kernel_1d = scipy.signal.boxcar(factor)
# kernel_2d = numpy.outer(kernel_1d, kernel_1d)

# c = scipy.signal.convolve(b, kernel_2d, mode="same")
# print(c.shape)
# print(c)





import richdem as rd
import numpy as np


dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM.tif'
demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
a = np.asarray(demDS)
print(a.shape)
factor = 1197/1279
result = ndimage.zoom(a, factor, mode='nearest', grid_mode=True)
print(result.shape)



from osgeo import gdal, gdalconst, ogr

dem_tiff = gdal.Open(dem_path, gdalconst.GA_ReadOnly)

driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reshape.tif', 
                        result.shape[1], result.shape[0], 1, 
                        gdal.GDT_Float32)
out_ds.SetProjection(dem_tiff.GetProjection())
out_ds.SetGeoTransform(dem_tiff.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(result)
band.FlushCache()
band.ComputeStatistics(True)