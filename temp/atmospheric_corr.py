# https://medium.com/nerd-for-tech/atmospheric-correction-of-satellite-images-using-python-42128504afc3
# https://colab.research.google.com/drive/1DcwL8xAE1t5NnHuUXxtACFEBBgP64AvZ?usp=sharing#scrollTo=3lH7pMfjcRmr

# ESUN
# https://www.gisagmaps.com/landsat-8-atco/

# importing the required libraries
from osgeo import gdal
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
import elevation 
from matplotlib.pyplot import figure
import os

import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from rasterio.crs import CRS
import rioxarray as rxr
import earthpy as et

import fiona
import rasterio
import rasterio.mask



import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from rasterio.crs import CRS
import rioxarray as rxr
import earthpy as et
import geopandas as gpd
import xarray as xr
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep


"""
  Creating a  Dictionary with key as the "property" and value as 
  numerical value given in the file.
  example  {'REFLECTANCE_MULT_BAND_7 ': ' 1.6439E-03'}
"""

Landsat7_mlt_dict = {}
with open('/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_MTL.txt', 'r') as _:
    for line in _:
        line = line.strip()
        if line != 'END':
            key, value = line.split('=')
            Landsat7_mlt_dict[key] = value
print(Landsat7_mlt_dict)



# Improting Image class from PIL module 
from PIL import Image 
Image.MAX_IMAGE_PIXELS = None

"""
   Arg: 
      img_path_arr = (array of images path that to be masked)
      output_folder = Name of the folder in which all the masked
                                masked images to be stored
  Returns:
      paths = list of path of msked images
  
  Function working:
      First is create a folder named <output_folder>
      This function take a list of paths of the images to masked and
      save the msked image in the <output_folder>. It mask the 
      region over the bhopal in rectangular shape the rectange is 
      950 pixel long and 500 pixel wide.
"""

def apply_mask(img_path_arr, output_folder):
  os.makedirs(output_folder, exist_ok= True)
  paths = list()
  # Opens a image in RGB mode 
  for i, img in enumerate(img_path_arr):
    im = Image.open(img) 
      
    # Setting the points for cropped image 
    left = 1150
    top = 2800
    right = 2100
    bottom = 3300
      
    # Cropped image of above dimension 
    # (It will not change orginal image) 
    im1 = im.crop((left, top, right, bottom)) 
      
    # Save the image 
    output_filename = str(output_folder+'/masked_{}.tif'.format(i))
    im1.save(output_filename)
    paths.append(output_filename)
  #os.close(output_folder)
  return paths
  #import cv2 
  #plt.imshow(cv2.imread('crop.tif'))




"""
  Arg: 
      data_array= (array of masked images path )
      band = band number 

  Returns:
      new_data_array = array of the radiance value of single masked image
  
  Function working:
      First it get the 'B' and 'G' value from the dictionary that we created 
      for landsat7. Then  by looping through the each pixel it converted the 
      pixel value to the radiance. and the return this value as an array
"""


def dn_to_radiance(data_array, band)  :

  # getting the G value 
  channel_gain = float(Landsat7_mlt_dict['RADIANCE_MULT_BAND_'+str(band)+' '])

  # Getting the B value
  channel_offset = float(Landsat7_mlt_dict['RADIANCE_ADD_BAND_'+str(band)+' '])

  # creating a temp array to store the radiance value
  new_data_array = np.empty_like(data_array)

  #loooping through the image
  for i,row in enumerate(data_array):
    for j, col in enumerate(row):

      # checking if the pixel value is not nan, to avoid background correction 
      if data_array[i][j] != np.nan:
        new_data_array[i][j] = data_array[i][j] * channel_gain +channel_offset
  print(f'Radiance calculated for band {band}')
  return new_data_array



from math import cos
import math

"""
  Arg: 
        arr = (array of images path of which reflectance to be calculated)
        ESUN = ESUN value of the band
    Returns:
        paths = array of reflectance value of the image
    
    Function working:
        First it read the 'd' and 'phi' value form the L7 dictionary
        The apply the reflectance formula to each pixel
"""
def radiance_to_reflectance(arr,ESUN,):

  #getting the d value
  d = float(Landsat7_mlt_dict['EARTH_SUN_DISTANCE '])

  # calculating rh phi value from theta
  phi = 90 - float(Landsat7_mlt_dict['SUN_ELEVATION '])

  # creating the temp array
  new_data_array = np.empty_like(arr)

  # loop to finf the reflectance
  for i,row in enumerate(arr):
    for j, col in enumerate(row):
      if arr[i][j] != np.nan:
        new_data_array[i][j] = np.pi *arr[i][j] * d**2/ (ESUN *cos(phi*math.pi/180))
  print(f"Reflectance of Band calculated")
  return new_data_array




from matplotlib.backends.backend_pgf import PdfPages
"""Arg: 
      arr = (array of images to be plotted)
      bands = (ands of the images in correct order)
      output_filename = name of output files
      output_folder = name of the output folder
  
  Function working:
      First it create a folder with specified name, The it 
      plot the images in their respective colunmns. First column
      is RAW Image, second is DN to Radinace and third is the 
      Radiance to reflectance.
"""

def plot_figure(arr, bands, output_filename,output_folder):

  #creating a folder 
  os.makedirs(output_folder, exist_ok= True)

  #Setting the column the names
  cols = ['DN ', 'DN to Radiance', 'Radiance to Reflectance']

  #setting the row names
  rows = bands

  # increasing the font size of the plot text
  matplotlib.rcParams.update({'font.size': 22})

  # increasing the size of the plots
  fig, ax = plt.subplots(len(arr) ,3,figsize=(35,35), dpi =100)

  for axes, col in zip(ax[0], cols):
    axes.set_title(col)

  for axes, row in zip(ax[:,0], rows):
      axes.set_ylabel(row, rotation=0, size='large',)

  im_ratio = np.array(arr).shape[0]/np.array(arr).shape[1] #
  #fig(num=None, figsize=(5, 5), dpi=80, facecolor='w', edgecolor='k')

  #plotting the images
  for i,band in enumerate(arr):
    for j, img in enumerate(band):
      im1 = ax[i, j].imshow(arr[i][j], cmap ='Greys_r',) #row=0, col=0
      
      fig.colorbar(im1 ,ax=ax[i,j], fraction=0.02*im_ratio)
      if j==2:
        output_flname = str(output_folder+'/processed_{}.tif'.format(i))
        im = Image.fromarray(arr[i][j])

        #Saving the final reflactance image to use it in further code
        im.save(output_flname)

    print(f"Ploting {i+1} band")
  fig.tight_layout(pad=1.5)
  plt.show()
  plt.savefig(output_filename)
  #plt.close()
  


  

# creating the list of all image to be used
L7_images = ['/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B1.TIF',
          '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B2.TIF',
          '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B3.TIF',
          '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B4.TIF',
          '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B5.TIF',
          '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B7.TIF',
          
         ]

# creating the array of ESUN value in the increasing band order #Extra-terrestrial solar irradiation(ESUN)
ESUN_L7 = [1970, 1842, 1547, 1044,225.7,82.06]






imagelist = list()

# Applying the mask to the images
masked_image_list = apply_mask(L7_images,'L7_masked')

"""
  This loop take all the masked images and then use the above defined fuctions
  to calculate the reflectance and then plot it. In the nutsell
  is combine all the code given above.
"""
for i,img in enumerate(masked_image_list):
  gdal_data = gdal.Open(img)
  gdal_band = gdal_data.GetRasterBand(1)
 
  data_array = gdal_data.ReadAsArray().astype(np.float)

  # replace missing values if necessary
  if np.any(data_array == 0):
    data_array[data_array == 0] = np.nan
  if i <=4:
    radiance = dn_to_radiance(data_array,i+1)
    reflectance = radiance_to_reflectance(radiance,ESUN_L7[i])
  else:
    radiance = dn_to_radiance(data_array,i+2)
    reflectance = radiance_to_reflectance(radiance,ESUN_L7[i])
  imagelist.append([data_array,radiance, reflectance])
  np.save('nmpyarr', imagelist) 
  print(f'completed{i+1}')
  
#plot_figure(imagelist, ['Band 1            ', 'Band 2            ','Band 3            ','Band 4            '])
plot_figure(np.load('/content/nmpyarr.npy'), ['Band 1            ', 'Band 2            ','Band 3            ',
                                                'Band 4            ','Band 5            ','Band 7            '],'L7_B123457_gain_masked.png','L7_processed')




# ########################################################################################################################

# #Spectral radiance scaling

# """
#   Arg: 
#         data_arr = (array of images path of which radinace to be calculated)
#         band = band of the images
#     Returns:
#         paths = array of radinace value of the image
    
#     Function working:
#         First it read the 'Lmax' , 'Lmin', 'DN max' 'DNmin' value form the L7 dictionary
#         The apply the spectral radiance formula to each pixel
# """
# def dn_to_radiance_spectral(data_array, band)  :

#   # Getting th Lmax
#   Lmax = float(Landsat7_mlt_dict['RADIANCE_MAXIMUM_BAND_'+str(band)+' '])
  
#   # Getting th Lmin
#   Lmin = float(Landsat7_mlt_dict['RADIANCE_MINIMUM_BAND_'+str(band)+' '])
  
#   # Getting th DNmax
#   DNmax = float(Landsat7_mlt_dict['QUANTIZE_CAL_MAX_BAND_'+str(band)+' '])

#   #Getting the  DNmin
#   DNmin = float(Landsat7_mlt_dict['QUANTIZE_CAL_MIN_BAND_'+str(band)+' '])

#   new_data_array = np.empty_like(data_array)
#   for i,row in enumerate(data_array):
#     for j, col in enumerate(row):
#       if data_array[i][j] != np.nan:
#         new_data_array[i][j] = ((Lmax - Lmin)*(data_array[i][j] - DNmin)/(DNmax-DNmin)) + Lmin
#   print(f'Radiance for band {band} is calculated using Specatral scaling')
#   return new_data_array





  
# # This code is same as above 
# L7_images = ['/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B1.TIF',
#           '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B2.TIF',
#           '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B3.TIF',
#           '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B4.TIF',
#           '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B5.TIF',
#           '/content/L7/LE07_L1TP_145044_20021210_20170127_01_T1_B7.TIF',
          
#          ]

# ESUN_L7 = [1970, 1842, 1547, 1044,225.7,82.06]

# imagelist = list()
# masked_image_list = apply_mask(L7_images,'L7_masked')

# for i,img in enumerate(masked_image_list):
#   gdal_data = gdal.Open(img)
#   gdal_band = gdal_data.GetRasterBand(1)
 
#   data_array = gdal_data.ReadAsArray().astype(np.float)

#   # replace missing values if necessary
#   if np.any(data_array == 0):
#     data_array[data_array == 0] = np.nan
#   if i <=4:
#     radiance = dn_to_radiance_spectral(data_array,i+1)
#     reflectance = radiance_to_reflectance(radiance,ESUN_L7[i])
#   else:
#     radiance = dn_to_radiance_spectral(data_array,i+2)
#     reflectance = radiance_to_reflectance(radiance,ESUN_L7[i])
#   imagelist.append([data_array,radiance, reflectance])
#   np.save('nmpyarr_3', imagelist) 
#   print(f'Completed calculation for band {i+1} ')




#   plot_figure(np.load('/content/nmpyarr_3.npy'), ['Band 1            ', 'Band 2            ','Band 3            ',
#                                                 'Band 4            ','Band 5            ','Band 7            '],'L7_B123457_Spectral_masked.png','L7_Processed_specteral')