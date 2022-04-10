from cProfile import label
from importlib.metadata import files
from pyexpat import features
from osgeo import gdal, gdalconst, ogr
import numpy as np
import richdem as rd


dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reshape.tif'  
demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
dem = np.asarray(demDS)

dem_class_bins = [-np.inf, 3000,3480, 3960, 4440, 4920, 5400, 5880, 6360, 6840, np.inf]
dem_landsat_class = np.digitize(dem, dem_class_bins)
dem_landsat_class = np.ma.masked_where(np.ma.getmask(dem), dem_landsat_class)
dem_1d = dem_landsat_class.flatten()


slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
slope_d = np.asarray(slope)

slope_class_bins = [-np.inf, 0, 2, 10, 30, 40, 90]
slope_landsat_class = np.digitize(slope_d, slope_class_bins)
slope_landsat_class = np.ma.masked_where(np.ma.getmask(slope_d), slope_landsat_class)
slope_1d = slope_landsat_class.flatten()



aspect = np.flipud(rd.TerrainAttribute(dem = demDS, attrib = 'aspect'))
aspect_d = np.asarray(aspect)

aspect_class_bins = [-np.inf, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, np.inf]
aspect_landsat_class = np.digitize(aspect_d, aspect_class_bins)

aspect_landsat_class = np.ma.masked_where(np.ma.getmask(aspect_d), aspect_landsat_class)
aspect_landsat_class = np.where(aspect_landsat_class == 9, 1, aspect_landsat_class)
aspect_1d = aspect_landsat_class.flatten()

import pandas as pd

df = pd.DataFrame({'elevation' : dem_1d,
                   'slope' : slope_1d,
                   'aspect' : aspect_1d})
print(df.shape)


from os import walk

files = []
for (dirpath, dirnames, filenames) in walk('E:/Dissertation/GFD/output/rishiganga/Extended'):
    files.extend(filenames)
    break

df_concat = pd.DataFrame()
data = []
morph = []
i=0
for file in files:
    file_path = f'E:/Dissertation/GFD/output/rishiganga/Extended/{file}'  
    file_DS = rd.LoadGDAL(filename = file_path, no_data = -9999.0)
    arr = np.asarray(file_DS)
    arr_1d = arr.flatten()

    df_lansat = pd.DataFrame(columns=['0'] )
    df_lansat['0'] = arr_1d
    data.append(df_lansat)
    i+=1
    morph.append(df)

print(df_lansat.shape)

df_land = pd.concat(data)
print(df_land.shape)

df_morph = pd.concat(morph)
print(df_morph.shape)




features = df_morph.values
label = df_land['0']

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3, random_state=49)

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)


from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
plot_confusion_matrix(gnb, X_test, y_test)  
plt.show()