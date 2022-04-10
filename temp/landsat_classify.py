# https://earthpy.readthedocs.io/en/latest/gallery_vignettes/plot_calculate_classify_ndvi.html

# import os
# from glob import glob
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.colors import ListedColormap
# import earthpy as et
# import earthpy.spatial as es
# import earthpy.plot as ep


# # Stack the Landsat 8 bands
# # This creates a numpy array with each "layer" representing a single band
# landsat_path = glob(
#     "E:/Dissertation/GFD/Landsat/LC08_L2SP_145039_20211003_20211013_02_T1_SR_B*.tif"
# )
# landsat_path.sort()
# arr_st, meta = es.stack(landsat_path, nodata=-9999)



# ## Calculate Normalized Difference Vegetation Index (NDVI) ##

# # Landsat 8 red band is band 4 at [3]
# # Landsat 8 near-infrared band is band 5 at [4]
# ndvi = es.normalized_diff(arr_st[3], arr_st[6])
# print(type(ndvi))


# ## Plot NDVI With Colorbar Legend of Continuous Values ##
# titles = ["Landsat 8 - Normalized Difference Vegetation Index (NDVI)"]

# # Turn off bytescale scaling due to float values for NDVI
# # ep.plot_bands(ndvi, cmap="jet", cols=1, title=titles, vmin=-1, vmax=1)

# print(ndvi[0][0])

# # print(max(ndvi))
# # print(min(ndvi))



from osgeo import gdal, gdalconst, ogr
import numpy as np

b1_tiff = gdal.Open("E:/Dissertation/GFD/Landsat/LC08_L2SP_145039_20211003_20211013_02_T1/LC08_L2SP_145039_20211003_20211013_02_T1_SR_B3.tif", gdalconst.GA_ReadOnly)
b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray())
# print(max(map(max,b1)))
# print(min(map(min,b1)))
# b1 = np.nan_to_num(b1, nan=-9999)
# print(type(b1))
# print(b1.shape)
b2_tiff = gdal.Open("E:/Dissertation/GFD/Landsat/LC08_L2SP_145039_20211003_20211013_02_T1/LC08_L2SP_145039_20211003_20211013_02_T1_SR_B6.tif", gdalconst.GA_ReadOnly)
b2 = np.array(b2_tiff.GetRasterBand(1).ReadAsArray())
# print(max(map(max,b2)))
# print(min(map(min,b2)))
# b2 = np.nan_to_num(b2, nan=-9999)
# print(type(b2))
# print(b2.shape)

ndsi1 = b1 - b2
ndsi2 = b1 + b2

ndsi = ndsi1/ndsi2
ndsi = np.nan_to_num(ndsi, nan=-9999)
ndsi = np.where(ndsi >1, -1, ndsi)
ndsi = np.where(ndsi <0.35, -1, ndsi)
ndsi = np.where(ndsi > 0, 1, ndsi)

# print(ndsi)
# print(max(map(max,ndsi)))
# print(min(map(min,ndsi)))



driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create("E:/Dissertation/GFD/output/landsat/LC08_L2SP_145039_20211003_20211013_02_T1.tiff", ndsi.shape[1], ndsi.shape[0], 1, gdal.GDT_Float32)
out_ds.SetProjection(b1_tiff.GetProjection())
out_ds.SetGeoTransform(b1_tiff.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(ndsi)
band.FlushCache()
band.ComputeStatistics(True)



import matplotlib.pyplot as plt

plt.imshow(ndsi, vmin=-1, vmax=1)
plt.set_cmap("magma") 
# plt.colorbar()
plt.title('NDSI LANDSAT-8')
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
plt.show()