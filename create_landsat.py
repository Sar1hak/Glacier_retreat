import os
from osgeo import gdal, gdalconst, ogr
import numpy as np
import warnings

## Suppressing warnings for cleaner dialogue box
warnings.simplefilter(action = 'ignore', category = FutureWarning)
warnings.simplefilter(action = 'ignore', category = RuntimeWarning)


dem_path = 'E:/Dissertation/RishiGanga/RishiGanga-Praveen/RishiGanga/RishiGanga_DEM_UTM44.tif'  
output_dem_path = "E:/Dissertation/GFD/output/rishiganga/Extended/RG_DEM.tif"
# data = gdal.Open(dem_path, gdalconst.GA_ReadOnly)
# geoTransform = data.GetGeoTransform()
# minx = geoTransform[0]
# maxy = geoTransform[3]
# maxx = minx + geoTransform[1] * data.RasterXSize
# miny = maxy + geoTransform[5] * data.RasterYSize

os.system(f'gdal_translate -projwin {str(371729.8003377388)} {str(3378992.0772707933)} {str(407644.7238875007)} {str(3349249.6088608615)} '
                            f'-a_nodata -9999.0 -of GTiff "{dem_path}" "{output_dem_path}"')

# print(f'{str(minx)} {str(maxy)} {str(maxx)} {str(miny)}' )
# import sys
# sys.exit()
print("... Read Digital Elevation model")


for root, dirs, files in os.walk(r'E:/Dissertation/GFD/Landsat'):
    
    if len(dirs)!=0:
        print("Found Existing FOlders")
        for landsat_dir in dirs:
            
            print("     " + landsat_dir, end="")
            filename_green = landsat_dir+ "/" + landsat_dir+ "_SR_B3.tif"
            filename_swir = landsat_dir+ "/" + landsat_dir+ "_SR_B6.tif"
            output_file_lansat = "E:/Dissertation/GFD/output/landsat/" + landsat_dir+ ".tif"
            output_file_rishiganga = "E:/Dissertation/GFD/output/rishiganga/Extended/" + landsat_dir+ ".tif"

            b1_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/Landsat/", filename_green), gdalconst.GA_ReadOnly)
            b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray())

            b2_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/Landsat/", filename_swir), gdalconst.GA_ReadOnly)
            b2 = np.array(b2_tiff.GetRasterBand(1).ReadAsArray())

            ndsi1 = b1 - b2
            ndsi2 = b1 + b2

            ndsi = ndsi1/ndsi2
            ndsi = np.nan_to_num(ndsi, nan = -9999)
            ndsi = np.where(ndsi > 1, -1, ndsi)
            ndsi = np.where(ndsi < 0.40, -1, ndsi)
            ndsi = np.where(ndsi > 0, 1, ndsi)


            driver = gdal.GetDriverByName("GTiff")
            out_ds = driver.Create(output_file_lansat, 
                                   ndsi.shape[1], ndsi.shape[0], 1, 
                                   gdal.GDT_Float32)
            out_ds.SetProjection(b1_tiff.GetProjection())
            out_ds.SetGeoTransform(b1_tiff.GetGeoTransform())
            band = out_ds.GetRasterBand(1)
            band.WriteArray(ndsi)
            band.FlushCache()
            band.ComputeStatistics(True)

            # os.system(f'gdal_translate -projwin {str(minx)} {str(maxy)} {str(maxx)} {str(miny)} '
            #                 f'-a_nodata -9999.0 -of GTiff "{output_file_lansat}" "{output_file_rishiganga}"')
            os.system(f'gdal_translate -projwin {str(371729.8003377388)} {str(3378992.0772707933)} {str(407644.7238875007)} {str(3349249.6088608615)} '
                            f'-a_nodata -9999.0 -of GTiff "{output_file_lansat}" "{output_file_rishiganga}"')
            
            print("     ...Files Created")

# gdal_translate -projwin 371729.8003377388 3378992.0772707933 407644.7238875007 3349249.6088608615 -of GTiff E:/Dissertation/GFD/output/landsat/LC08_L2SP_145039_20131029_20200912_02_T1.tif E:/Dissertation/GFD/qwqewf.tif
# "gdal_translate -projwin 371729.8003377388 3378992.0772707933 407644.7238875007 3349249.6088608615 -a_nodata -9999.0 -of GTiff E:/Dissertation/GFD/ndsi1.tiff C:/Users/Sarthak/AppData/Local/Temp/processing_OYLeXs/95f45cb28f6b4cfea4710570c58567df/OUTPUT.tif"
# "gdal_translate -projwin 369328.3565 3389989.349 413756.9134 3340926.9667 -a_nodata -9999.0 -of GTiff E:/Dissertation/GFD/output/landsat/LC08_L2SP_145039_20131029_20200912_02_T1.tif C:/Users/Sarthak/AppData/Local/Temp/processing_OYLeXs/8861145e9845485eb912cc08cf013656/OUTPUT.tif"

# "gdal_translate -projwin 369328.3565 3389989.349 413756.9134 3340926.9667 -a_nodata -9999.0 -of GTiff E:/Dissertation/GFD/output/landsat/LC08_L2SP_145039_20140914_20200911_02_T1.tif C:/Users/Sarthak/AppData/Local/Temp/processing_OYLeXs/d6816a87848d408ab95a576ba7962027/OUTPUT.tif"