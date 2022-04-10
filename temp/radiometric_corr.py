from osgeo import gdal
import numpy as np
import sys
import math

def dos(input, output):
    """
        Skyradiance/Haze/Dark Object Subtraction
    """
    image = gdal.Open(input)
    if image is None:
        print ('Unable to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName("GTiff")
    outdata = outdriver.Create(str(outfile), rows, cols, image.RasterCount, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        stats = image.GetRasterBand(band).GetStatistics(True, True)
        minimum = stats[0]
        bandarray = np.array(image.GetRasterBand(band).ReadAsArray())
        outdata.GetRasterBand(band).WriteArray(bandarray - minimum)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)

def sac(input, output, angle):
    """
        Sun Angle Correction
    """
    image = gdal.Open(input)
    if image is None:
        print ('Unble to open the source file')
        sys.exit()
    [cols, rows] = np.array(image.GetRasterBand(1).ReadAsArray()).shape
    trans = image.GetGeoTransform()
    proj = image.GetProjection()
    outfile = output
    outdriver = gdal.GetDriverByName('GTiff')
    outdata = outdriver.Create(str(outfile), rows, cols, 4, gdal.GDT_Float32)
    for band in range(image.RasterCount):
        band += 1
        bandarray = np.array(image.GetRasterBand(band).ReadAsArray())
        bandarray1 = bandarray / math.sin(angle)
        outdata.GetRasterBand(band).WriteArray(bandarray1)
        outdata.SetGeoTransform(trans)
        outdata.SetProjection(proj)
