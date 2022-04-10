# https://www.programmerall.com/article/11722246140/
# https://www.youtube.com/watch?v=cWfj9B9mJ4E
from osgeo import gdal
from osgeo import osr

dataset = gdal.Open(r'xxx.tif', gdal.GA_Update)


#  The actual control point is definitely more, and only four points are written here. Be better interactions with adult machines.
gcps_list = [gdal.GCP(-111.931075, 41.745836, 0, 1078, 648),
             gdal.GCP(-111.901655, 41.749269, 0, 3531, 295),
             gdal.GCP(-111.899180, 41.739882, 0, 3722, 1334),
             gdal.GCP(-111.930510, 41.728719, 0, 1102, 2548)]




gdal.GCP([x], [y], [z], [pixel], [line], [info], [id])
#  X, Y, Z is the projection coordinates corresponding to the control point, and it is default to zero;
#  Pixel, line is the column, line location, default to 0;
#  INFO, ID is an optional string for explaining a description of the control point and the point number, which is empty.



sr = osr.SpatialReference()
sr.SetWellKnownGeogCS('WGS84')
#  Add control point
dataset.SetGCPs(gcps, sr.ExportToWkt())


#  TPS Correction Sampling: Normal Near
dst_ds = gdal.Warp(r'xxx_dst.tif', dataset, format='GTiff', tps=True, 
                   xRes=0.05, yRes=0.05, dstNodata=65535, srcNodata=65535, 
                   resampleAlg=gdal.GRIORA_NearestNeighbour， outputType=gdal.GDT_Int32)


# ds = gdal.Warp(r'X:\ModisNearest.tif',
#                r'HDF4_EOS:EOS_SWATH:"X:\MOD021KM.A2018130.0220.061.2018130132414\MOD021KM.A2018130.0220.061.2018130132414.hdf":MODIS_SWATH_Type_L1B:EV_1KM_RefSB',
#                width=2030, height=1354, format='GTiff', geoloc=True,
#                dstSRS=sr.ExportToWkt(), resampleAlg=gdal.GRIORA_NearestNeighbour)