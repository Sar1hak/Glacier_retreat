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

def input_layer(input_shape = 1, droput_rate = 0.0):
    input = Input(shape = (input_shape,))
    layer = Dense(1, activation = 'relu',
                        kernel_initializer = 'he_normal')(input)
    output_layer = Dropout(droput_rate)(layer)
    return output_layer


def merger(hgt_layer, slope_layer, asp_layer, glac_layer):

    merge_1 = Concatenate([hgt_layer, slope_layer])
    merged_2 = Concatenate([merge_1, asp_layer])
    merged_features = Concatenate([merged_2, glac_layer])
    model = Model(inputs = [hgt_layer, slope_layer, asp_layer, glac_layer], 
                  outputs = merged_features)

    return model

hgt_layer, slope_layer, asp_layer, glac_layer = input_layer(1, prob_dem), input_layer(1, prob_slope), input_layer(1, prob_asp), input_layer(1, prob_init_glac)
model = merger(hgt_layer, slope_layer, asp_layer, glac_layer)
model.add(Dense(16, activation = 'relu'))
model.add(Dense(32, activation = 'relu'))
model.add(Dense(64, activation = 'relu'))
model.add(Dense(32, activation = 'relu'))
model.add(Dense(16, activation = 'relu'))

model.add(Dense(1, activation = 'sigmoid'))

plot_model(model,
           to_file="model.png",
           show_shapes=True,
           show_layer_names=True,)



model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
model.fit([hgt_train, slope_train, asp_train, glac_train], y_train, batch_size = 32, epochs = 100)
y_pred = model.predict([hgt_test, slope_test, asp_test, glac_test])
y_pred = (y_pred > 0.5)
