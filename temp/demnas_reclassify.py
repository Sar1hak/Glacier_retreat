import os
from osgeo import gdal
from osgeo import osr
import numpy

# config
GDAL_DATA_TYPE = gdal.GDT_Int32 
GEOTIFF_DRIVER_NAME = r'GTiff'
NO_DATA = 15
SPATIAL_REFERENCE_SYSTEM_WKID = 4326

def create_raster(output_path,
                  columns,
                  rows,
                  nband = 1,
                  gdal_data_type = GDAL_DATA_TYPE,
                  driver = GEOTIFF_DRIVER_NAME):
    ''' returns gdal data source raster object

    '''
    # create driver
    driver = gdal.GetDriverByName(driver)

    output_raster = driver.Create(output_path,
                                  int(columns),
                                  int(rows),
                                  nband,
                                  eType = gdal_data_type)    
    return output_raster

def numpy_array_to_raster(output_path,
                          numpy_array,
                          upper_left_tuple,
                          cell_resolution,
                          nband = 1,
                          no_data = NO_DATA,
                          gdal_data_type = GDAL_DATA_TYPE,
                          spatial_reference_system_wkid = SPATIAL_REFERENCE_SYSTEM_WKID,
                          driver = GEOTIFF_DRIVER_NAME):
    ''' returns a gdal raster data source

    keyword arguments:

    output_path -- full path to the raster to be written to disk
    numpy_array -- numpy array containing data to write to raster
    upper_left_tuple -- the upper left point of the numpy array (should be a tuple structured as (x, y))
    cell_resolution -- the cell resolution of the output raster
    nband -- the band to write to in the output raster
    no_data -- value in numpy array that should be treated as no data
    gdal_data_type -- gdal data type of raster (see gdal documentation for list of values)
    spatial_reference_system_wkid -- well known id (wkid) of the spatial reference of the data
    driver -- string value of the gdal driver to use

    '''

    rows, columns = numpy_array.shape


    # create output raster
    output_raster = create_raster(output_path,
                                  int(columns),
                                  int(rows),
                                  nband,
                                  gdal_data_type) 

    geotransform = (upper_left_tuple[0],
                    cell_resolution,
                    upper_left_tuple[1] + cell_resolution,
                    -1 *(cell_resolution),
                    0,
                    0)

    spatial_reference = osr.SpatialReference()
    spatial_reference.ImportFromEPSG(spatial_reference_system_wkid)
    output_raster.SetProjection(spatial_reference.ExportToWkt())
    output_raster.SetGeoTransform(geotransform)
    output_band = output_raster.GetRasterBand(1)
    output_band.SetNoDataValue(no_data)
    output_band.WriteArray(numpy_array)          
    output_band.FlushCache()
    output_band.ComputeStatistics(False)

    if os.path.exists(output_path) == False:
        raise Exception('Failed to create raster: %s' % output_path)

    return  output_raster




################################################################
from osgeo import gdal
from osgeo import osr
import richdem as rd
import numpy as np

def demnas_reclass(dem_loc):

    # dataset = gdal.Open(dem_loc, gdal.GA_Update)
    dataset = rd.LoadGDAL(filename = dem_loc, no_data = -9999.0)

    slope = rd.TerrainAttribute(dataset, attrib = 'slope_degrees')
    rd.SaveGDAL("mydem_filled.tif", slope)

    aspect = np.flipud(rd.TerrainAttribute(dem = dataset, attrib = 'aspect'))
    rd.SaveGDAL("mydem_filled.tif", aspect)


import os

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import xarray as xr
import rioxarray as rxr
# import earthpy as et
# import earthpy.plot as ep


slope_class_bins = [-np.inf, 2, 8, 19, 37, np.inf]
elevation_class_bins = [-np.inf, 4810, 4770, 4720, 4670, 4620, 4570, 4520, 4470, np.inf]
peak_class_bins = [-np.inf, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2300, 2600, np.inf]
aspect_class_bins = [-np.inf, 22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5, np.inf]


def reclass_range(tiff_loc, class_bins):
    pre_lidar_chm = rxr.open_rasterio(tiff_loc, masked=True).squeeze()
    # Check nodata value for your array
    pre_lidar_chm.rio.nodata

    # class_bins = [-np.inf, 2, 7, 12, np.inf]
    
    pre_lidar_chm_class = xr.apply_ufunc(np.digitize,
                                     pre_lidar_chm,
                                     class_bins)
    # Mask out values not equal to last class
    pre_lidar_chm_class_ma = pre_lidar_chm_class.where(pre_lidar_chm_class != len(class_bins))

    # Plot data using nicer colors
    colors = ['linen', 'lightgreen', 'darkgreen', 'maroon']
    class_bins = [.5, 1.5, 2.5, 3.5, 4.5]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(class_bins, 
                        len(colors))

    # Plot newly classified and masked raster
    f, ax = plt.subplots(figsize=(10, 5))
    pre_lidar_chm_class_ma.plot.imshow(cmap=cmap,
                                    norm=norm)
    ax.set(title="Classified Plot With a Colorbar and Custom Colormap (cmap)")
    ax.set_axis_off()
    plt.show()

import richdem as rd
import numpy as np
import os
def create_file(dem_path):
    slope_path = os.getcwd() + '/temp/slope.tif'
    aspect_path = os.getcwd() + '/temp/aspect.tif'
    
    demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
    slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
    rd.SaveGDAL(slope_path, slope)

    ## Calculate aspect from DEM
    aspect = np.flipud(rd.TerrainAttribute(dem = demDS, attrib = 'aspect'))
    rd.SaveGDAL(aspect_path, slope)


if __name__ == "__main__":

    file_name = ""
    create_file()
