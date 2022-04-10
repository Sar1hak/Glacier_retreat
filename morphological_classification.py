import richdem as rd
import numpy as np
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import earthpy.plot as ep


from osgeo import gdal, gdalconst, ogr

dem_tiff = gdal.Open('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reshape.tif', gdalconst.GA_ReadOnly)



dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reshape.tif'  
slope_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/slope.tif'
aspect_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/aspect.tif'



demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
dem = np.asarray(demDS)
rd.rdShow(demDS, axes = False, cmap='magma', figsize=(8,5.5))

# print(dem)
# print(dem.shape)
# rd.FillDepressions(demDS, epsilon=False, in_place=True)
# rd.rdShow(demDS, axes=False, cmap='jet', figsize=(8,5.5))

print(max(map(max,dem)))
print(min(map(min,dem)))

# plt.imshow(slope_d, vmin=89.9, vmax=90)
# plt.set_cmap("rainbow") 
# plt.show()


ndvi_class_bins = [-np.inf, 3000,3480, 3960, 4440, 4920, 5400, 5880, 6360, 6840, np.inf]
ndvi_landsat_class = np.digitize(dem, ndvi_class_bins)
print(type(ndvi_landsat_class))
print(np.unique(ndvi_landsat_class))



driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reclass.tif', 
                        ndvi_landsat_class.shape[1], ndvi_landsat_class.shape[0], 1, 
                        gdal.GDT_Float32)
out_ds.SetProjection(dem_tiff.GetProjection())
out_ds.SetGeoTransform(dem_tiff.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(ndvi_landsat_class)
band.FlushCache()
band.ComputeStatistics(True)


# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(np.ma.getmask(dem), ndvi_landsat_class)
print(type(ndvi_landsat_class))
# rd.SaveGDAL('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reclass.tif', np.array(ndvi_landsat_class))

print(np.unique(ndvi_landsat_class))


# Define color map
nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen",'red',"maroon", "blue", "black", "yellow"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "< 3000",
    "3000 - 3480",
    "3480 - 3960",
    "3960 - 4440",
    "4440 - 4920",
    "4920 - 5400",
    "5400 - 5880",
    "5880 - 6360",
    "6360 - 6840",
    "6840 >"
]

# Get list of classes
classes = np.unique(ndvi_landsat_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:10]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    "Landsat 8 - Elevation Classes",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()
plt.show()

########################################################################################################################################











slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
# slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
slope_d = np.asarray(slope)
print(max(map(max,slope_d)))
print(min(map(min,slope_d)))

# plt.imshow(slope_d, vmin=89.9, vmax=90)
# plt.set_cmap("rainbow") 
# plt.show()


rd.SaveGDAL(slope_path, slope)
rd.rdShow(slope, axes = False, cmap='rainbow', figsize=(8,5.5))

# ndvi_class_bins = [-np.inf, 89, 89.995, 89.996,89.997, 89.998,89.9985, 90]
ndvi_class_bins = [0, 2, 10, 30, 40, 90]

ndvi_landsat_class = np.digitize(slope_d, ndvi_class_bins)
print(np.unique(ndvi_landsat_class))


driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_SLP_reclass.tif', 
                        ndvi_landsat_class.shape[1], ndvi_landsat_class.shape[0], 1, 
                        gdal.GDT_Float32)
out_ds.SetProjection(dem_tiff.GetProjection())
out_ds.SetGeoTransform(dem_tiff.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(ndvi_landsat_class)
band.FlushCache()
band.ComputeStatistics(True)



# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(
    np.ma.getmask(slope_d), ndvi_landsat_class
)
# rd.SaveGDAL('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_SLP_reclass.tif', ndvi_landsat_class)
print(np.unique(ndvi_landsat_class))



## Plot Classified NDVI With Categorical Legend - EarthPy Draw_Legend() ##

# Define color map
# nbr_colors = ["gray", "pink", "yellowgreen", "g", "darkgreen",'red', "blue"]
nbr_colors = ["grey", "yellowgreen", "pink", "darkgreen",'red', "blue"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "0 - 2",
    "2 - 10",
    "10 - 30",
    "30 - 40",
    "40 >"
]
# ndvi_cat_names = [
#     "89 <",
#     "89 - 89.995",
#     "89.995 - 89.996",
#     "89.996 - 89.997",
#     "89.997 - 89.998",
#     "89.998 - 89.9985",
#     "89.9985 >"
# ]

# Get list of classes
classes = np.unique(ndvi_landsat_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:7]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    "Landsat 8 - Slope Classes",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()
plt.show()



######################################################################################################################################














# ## Calculate aspect from DEM
aspect = np.flipud(rd.TerrainAttribute(dem = demDS, attrib = 'aspect'))
aspect_d = np.asarray(aspect)
print(max(map(max,aspect_d)))
print(min(map(min,aspect_d)))

rd.SaveGDAL(aspect_path, aspect)
rd.rdShow(aspect, axes=False, cmap='viridis', figsize=(8,5.5))


ndvi_class_bins = [-np.inf, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, np.inf]
ndvi_landsat_class = np.digitize(aspect_d, ndvi_class_bins)
ndvi_landsat_class = np.where(ndvi_landsat_class==9, 1, ndvi_landsat_class)

print(np.unique(ndvi_landsat_class))


driver = gdal.GetDriverByName("GTiff")
out_ds = driver.Create('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_ASP_recalss.tif', 
                        ndvi_landsat_class.shape[1], ndvi_landsat_class.shape[0], 1, 
                        gdal.GDT_Float32)
out_ds.SetProjection(dem_tiff.GetProjection())
out_ds.SetGeoTransform(dem_tiff.GetGeoTransform())
band = out_ds.GetRasterBand(1)
band.WriteArray(ndvi_landsat_class)
band.FlushCache()
band.ComputeStatistics(True)





# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(
    np.ma.getmask(aspect_d), ndvi_landsat_class
)
# rd.SaveGDAL('E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_ASP_reclass.tif', ndvi_landsat_class)

print(np.unique(ndvi_landsat_class))
print(max(map(max,ndvi_landsat_class)))
print(min(map(min,ndvi_landsat_class)))


## Plot Classified NDVI With Categorical Legend - EarthPy Draw_Legend() ##

# Define color map
nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen",'red', "blue", "black", "yellow"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "North",
    "Northeast",
    "East",
    "Southeast",
    "South",
    "Southwest",
    "West",
    'Northwest',
]

# Get list of classes
classes = np.unique(ndvi_landsat_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:8]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    "Landsat 8 - Aspect Classes",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()
plt.show()
