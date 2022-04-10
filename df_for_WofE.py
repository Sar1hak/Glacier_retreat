# import pandas as pd
# import os
# from osgeo import gdal, gdalconst, ogr
# import numpy as np
# import warnings
# import richdem as rd

# dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reclass.tif'  
# slope_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_SLP_reclass.tif'
# aspect_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_ASP_recalss.tif'


# demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
# dem = np.asarray(demDS).flatten()
# slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
# slope_d = np.asarray(slope).flatten()
# aspect = np.flipud(rd.TerrainAttribute(dem = demDS, attrib = 'aspect'))
# aspect_d = np.asarray(aspect).flatten()


# df = pd.DataFrame(columns=['Year', 'Elevation', 'Slope', 'Aspect', 'GR'])




# dir_list = os.listdir('E:/Dissertation/GFD//output/rishiganga/Extended')
# # c = 2013
# for landsat_dir in dir_list:
#     try:
#         print(landsat_dir)

#         b1_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/output/rishiganga/Extended/", landsat_dir), gdalconst.GA_ReadOnly)
#         b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray()).flatten()

#     except:
#         print('error')
#         continue

#     df_1 = pd.DataFrame({'Year': [landsat_dir[17:21] for i in range(0, len(b1))],
#                          'Elevation':dem,
#                          'Slope': slope_d,
#                          'Aspect': aspect_d,
#                          'GR': b1})
#     print(landsat_dir[17:21])
#     df = pd.concat([df, df_1], axis=0)

# print(df.shape)
# df.to_csv('E:/Dissertation/GFD//output/rishiganga/Extended/dem/Data_frame.csv')






























import pandas as pd
import os
from osgeo import gdal, gdalconst, ogr
import numpy as np
import warnings
import richdem as rd

dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reclass.tif'  
slope_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_SLP_reclass.tif'
aspect_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_ASP_recalss.tif'


demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
dem = np.asarray(demDS).flatten()
slope = rd.LoadGDAL(filename = slope_path, no_data = -9999.0)
slope_d = np.asarray(slope).flatten()
aspect = rd.LoadGDAL(filename = aspect_path, no_data = -9999.0)
aspect_d = np.asarray(aspect).flatten()


df = pd.DataFrame(columns=['Year', 'Elevation', 'Slope', 'Aspect', 'GR'])




dir_list = os.listdir('E:/Dissertation/GFD//output/rishiganga/Extended')
# c = 2013

for landsat_dir in dir_list:
    try:
        print(landsat_dir)

        b1_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/output/rishiganga/Extended/", landsat_dir), gdalconst.GA_ReadOnly)
        b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray()).flatten()

    except:
        print('error')
        continue

    df_1 = pd.DataFrame({'Year': [landsat_dir[17:21] for i in range(0, len(b1))],
                         'Elevation':dem,
                         'Slope': slope_d,
                         'Aspect': aspect_d,
                         'GR': b1})
    print(landsat_dir[17:21])
    if os.path.isfile(f'E:/Dissertation/GFD//output/rishiganga/Extended/dem/Dataframes/{landsat_dir[17:21]}.csv') is False:
        df_1.to_csv(f'E:/Dissertation/GFD//output/rishiganga/Extended/dem/Dataframes/{landsat_dir[17:21]}.csv')
        temp = df_1
    else:
        df = pd.concat([temp, df_1], axis=0)
        df.to_csv(f'E:/Dissertation/GFD//output/rishiganga/Extended/dem/Dataframes/{landsat_dir[17:21]}.csv')
        temp = df































