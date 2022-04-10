
import pandas as pd
import os
from osgeo import gdal, gdalconst, ogr
import numpy as np
import warnings
import richdem as rd

temp = 0
dir_list = os.listdir('E:/Dissertation/GFD//output/rishiganga/Extended')
glacier_area = []
for landsat_dir in dir_list:
    try:
        if landsat_dir[17:21] != temp:
            b1_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/output/rishiganga/Extended/", landsat_dir), gdalconst.GA_ReadOnly)
            b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray())
            b1 = np.where(b1 == 1, 1, -1)
            print(landsat_dir)
            sat_unique, sat_count = np.unique(b1, return_counts=True)
            glacier_area.append(sat_count[1])
            temp = landsat_dir[17:21]

    except:
        print('error')
        continue


import matplotlib.pyplot as plt

plt.plot([x for x in range(2013,2024)],glacier_area)
plt.show()