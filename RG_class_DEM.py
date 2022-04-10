import os
from osgeo import gdal, gdalconst, ogr
import numpy as np
import warnings

land_path = 'E:/Dissertation/GFD/output/rishiganga/LC08_L2SP_145039_20131029_20200912_02_T1.tif'  

dem_path = 'E:/Dissertation/RishiGanga/RishiGanga-Praveen/RishiGanga/RishiGanga_DEM_UTM44.tif'  

land_data = gdal.Open(land_path, gdalconst.GA_ReadOnly)

# dem_data = gdal.Open(dem_path, gdalconst.GA_ReadOnly)
output_file_rishiganga = 'E:/Dissertation/GFD/output/rishiganga/dem/DEM_UTM44_converted.tif'

geoTransform = land_data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * land_data.RasterXSize
miny = maxy + geoTransform[5] * land_data.RasterYSize


os.system(f'gdal_translate -projwin {str(minx)} {str(maxy)} {str(maxx)} {str(miny)} '
                f'-a_nodata -9999.0 -of GTiff "{dem_path}" "{output_file_rishiganga}"')
