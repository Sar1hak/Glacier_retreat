import numpy as np
import pandas as pd
import richdem as rd
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import (Concatenate, Dense, Dropout, Input,
                                     Sequential)
from tensorflow.keras.models import Model
from tensorflow.keras.utils import plot_model

prob_dem = 0.50
dem_path = 'E:/Dissertation/GFD/output/rishiganga/dem/DEM_UTM44_converted.tif'  
demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
dem_2d = np.asarray(demDS)
dem_1d = dem_2d.flatten()

prob_slope = 0.50
slope_path = 'E:/Dissertation/GFD/output/rishiganga/dem/Slope_converted.tif'  
slopeDS = rd.LoadGDAL(filename = slope_path, no_data = -9999.0)
slope_2d = np.asarray(slopeDS)
slope_1d = slope_2d.flatten()

prob_asp = 0.50
asp_path = 'E:/Dissertation/GFD/output/rishiganga/dem/aspect_converted.tif'  
aspDS = rd.LoadGDAL(filename = asp_path, no_data = -9999.0)
aspect_2d = np.asarray(aspDS)
aspect_1d = aspect_2d.flatten()

glac_path = 'E:/Dissertation/GFD/output/rishiganga/dem/aspect_converted.tif'
glacDS = rd.LoadGDAL(filename = glac_path, no_data = -9999.0)
glac_features_2d = np.asarray(glacDS)
glac_features_1d = glac_features_2d.flatten()

prob_init_glac = 0.50
inital_glac_features = np.zeros(glac_features_1d.shape)

df = pd.DataFrame({'Elevation': dem_1d,
                   'Slope': slope_1d,
                   'Aspect': aspect_1d,
                   'Initial_glacier_cover': inital_glac_features,
                   'Glacier_Cover': glac_features_1d})

X = df[ : ,0 : -1].values
y  =df[:, -1].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=49)


hgt_train, hgt_test = X_train[:, 0], X_test[:, 0]
slope_train, slope_test = X_train[:, 1], X_test[:, 1]
asp_train, asp_test = X_train[:, 2], X_test[:, 2]
glac_train, glac_test = X_train[:, 3], X_test[:, 3]




from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
model = Sequential()
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28,28,1)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(10, activation='softmax'))