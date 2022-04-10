# import os
# from osgeo import gdal, gdalconst, ogr
# import numpy as np
# import warnings
# import richdem as rd

# dem_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_DEM_reclass.tif'  
# slope_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_SLP_reclass.tif'
# aspect_path = 'E:/Dissertation/GFD/output/rishiganga/Extended/dem/RG_ASP_recalss.tif'


# demDS = rd.LoadGDAL(filename = dem_path, no_data = -9999.0)
# dem = np.asarray(demDS)
# slope = rd.TerrainAttribute(demDS, attrib='slope_degrees')
# slope_d = np.asarray(slope)
# aspect = np.flipud(rd.TerrainAttribute(dem = demDS, attrib = 'aspect'))
# aspect_d = np.asarray(aspect)


# DEM_count, SLP_count, ASP_count = [], [], []
# DEM_unik, SLP_unik, ASP_unik = [], [], []

# dir_list = os.listdir('E:/Dissertation/GFD//output/rishiganga/Extended')
# print("Found Existing Folders")
# for landsat_dir in dir_list:

#     try:
#         print("     " + landsat_dir)
#         # filename = landsat_dir+ ".tif"
#         # print(filename)
#         b1_tiff = gdal.Open(os.path.join("E:/Dissertation/GFD/output/rishiganga/Extended/", landsat_dir), gdalconst.GA_ReadOnly)
#         b1 = np.array(b1_tiff.GetRasterBand(1).ReadAsArray())

#     except:
#         print('error')
#         continue

#     # print("sfg")
#     # indices = list(filter(lambda x: x == 'whatever', b1))
#     stack_dem = np.where(b1==1, dem, -9999)
#     dem_unique, dem_count = np.unique(stack_dem, return_counts=True)
#     print("Unique values:", dem_unique)
#     print("Counts:", dem_count)
#     dem_count = np.delete(dem_count, 0)
#     DEM_count.append(dem_count)
#     dem_unique = np.delete(dem_unique, 0)
#     DEM_unik.append(dem_unique)

#     # stack_slope = np.where(b1==1, slope_d, -9999)
#     # slope_unique, slope_count = np.unique(stack_slope, return_counts=True)
#     # print("Unique values:", slope_unique)
#     # print("Counts:", slope_count)
#     # slope_count = np.delete(slope_count, 0)
#     # SLP_count.append(dem_count)
#     # slope_unique = np.delete(slope_unique, 0)
#     # SLP_unik.append(slope_unique)
    
#     # stack_aspect = np.where(b1==1, aspect_d, -9999)
#     # aspect_unique, aspect_count = np.unique(stack_aspect, return_counts=True)
#     # print("Unique values:", aspect_unique)
#     # print("Counts:", aspect_count)
#     # aspect_count = np.delete(aspect_count, 0)
#     # ASP_count.append(dem_count)
#     # aspect_unique = np.delete(aspect_unique, 0)
#     # ASP_unik.append(aspect_unique)
    
# print("#######################")

# import pandas as pd
# DEM_cat_names = [
#     "< 3000",
#     "3000 - 3480",
#     "3480 - 3960",
#     "3960 - 4440",
#     "4440 - 4920",
#     "4920 - 5400",
#     "5400 - 5880",
#     "5880 - 6360",
#     "6360 - 6840",
#     "6840 >"
# ]

# df = pd.DataFrame(columns=DEM_cat_names,index= [str(i) for i in range(2013, 2022)])

# for x in range(-0.1,10):
#     dem_x = [i for i in range(1,11)]
#     if len(DEM_unik[x])!=dem_x:
#         for j in range(-0.1,10):
#             if DEM_unik[x][j]!=dem_x[j]:
#                 DEM_unik[x] = np.insert(DEM_unik[x], j , dem_x[j])
#                 DEM_count[x] = np.insert(DEM_count[x], j ,0)

#     df.loc[str(x+2013)] = DEM_count[x]
#     print(DEM_count[x])

# print(df.shape)
# print(df)


# df.plot(kind="bar",figsize=(15, 8))

# import matplotlib.pyplot as plt
# plt.title("Elevation and Glacier Retreat association")

# plt.xlabel("Year")

# plt.ylabel("Category Count")

# plt.show()



import sys
import pandas as pd
import matplotlib.pyplot as plt



df_DEM = pd.DataFrame({"2013":[-0.1, -0.1, -0.1, -4.53387, -1.862138, -0.222278,1.280001, 1.719752, 2.192961, 2.086018],
                       "2014":[-0.1, -0.1, -6.121298, -7.927163, -1.822402, 0.11055, 1.110254, 1.770599, 3.094261, 4.462261],
                       "2015":[-0.1, -0.1, -0.1, -0.1, -3.105716, -0.602054, 1.145958, 1.957459, 3.042545, 5.267786],
                       "2016":[-0.1, -0.1, -0.1, -5.068528, -3.302252, -0.774905, 1.097598, 2.00559, 3.102512, 3.827193],
                       "2017":[-0.1, -0.1, -0.1, -0.1, -3.805541, -0.526726, 1.094783, 1.838847, 2.87242, 2.95984],
                       "2018":[-0.1, -0.1, -0.1, -7.920063, -3.632563, -0.699871, 1.145336, 2.005075, 3.352494, 5.692103],
                       "2019":[-0.1, -8.145861, -5.184447, -4.331376, -1.638592, 0.628045, 1.741747, 2.049002, 2.701265, 5.243349],
                       "2020":[-0.1, -0.1, -0.1, -0.1, -3.052785, -0.520151, 1.055045, 1.718998, 2.816148, 3.075988],
                       "2021":[-0.1, -4.463756, -4.158457, -4.720049, -2.833335, -0.325365, 1.17985, 1.922716, 2.806248, 2.718345]
                       },
                       index = ["< 3000",
                                "3000 - 3480",
                                "3480 - 3960",
                                "3960 - 4440",
                                "4440 - 4920",
                                "4920 - 5400",
                                "5400 - 5880",
                                "5880 - 6360",
                                "6360 - 6840",
                                "6840 >"])

plt.rc('axes', labelsize=15,  titlesize=20) 

df_DEM.plot(kind="bar")

plt.title("Elevation and Glacier Retreat association")
plt.xlabel("Elevation Class")
plt.xticks(rotation=0)
plt.ylabel("Weight of Evidence (WofE)")

plt.show()



# import sys
# sys.exit()





df_Slp = pd.DataFrame({"2013":[1.172919,1.020428, 0.370216, -0.397246, -0.38273],
                       "2014":[1.008043,0.802181, 0.200939, -0.462215, -0.085373],
                       "2015":[0.895425,0.756568, 0.246682, -0.368209, -0.158526],
                       "2016":[1.098069, 0.874847, 0.24385, -0.386806, -0.186717],
                       "2017":[1.248208, 1.014846, 0.339051, -0.398358, -0.33727],
                       "2018":[0.883293, 0.649362, 0.14416, -0.399409, -0.033462],
                       "2019":[1.10043, 1.142823, 0.24122, -0.472829, -0.118775],
                       "2020":[1.262979, 1.026617, 0.332031, -0.371153, -0.362014],
                       "2021":[1.072523, 0.911623, 0.314219, -0.407005, -0.246193]
                       },
                       index = [
                                "0 - 2",
                                "2 - 10",
                                "10 - 30",
                                "30 - 40",
                                "40 >"
                                ])

plt.rc('axes', labelsize=15,  titlesize=20) 
df_Slp.plot(kind="bar")

plt.title("Slope and Glacier Retreat association")
plt.xlabel("Slope Class")
plt.xticks(rotation=0)
plt.ylabel("Weight of Evidence (WofE)")

plt.show()

















df_Asp = pd.DataFrame({"2013":[-0.013247, -0.125869, 0.06932, 0.503018, 0.434673, -0.472462, -0.708792, -0.168044],

                       "2014":[0.001051,-0.066531,0.014783,0.535132,0.478929,-0.39419,-0.719969,-0.325743],
                       "2015":[0.013016,-0.00754,0.14037,0.456719,0.383902,-0.472526,-0.742558,-0.345778],
                       "2016":[0.013034,-0.037972,0.110369,0.518201,0.376054,-0.558129,-0.732991,-0.34162],
                       "2017":[-0.051114,-0.086732,0.112378,0.574516,0.407614,-0.574867,-0.753816,-0.353301],
                       "2018":[-0.040529,-0.018257,0.228674,0.604587,0.320207,-0.697056,-0.932119,-0.353076],
                       "2019":[0.01047,0.047559,0.157485,0.297525,0.198593,-0.422607,-0.432463,-0.089059],
                       "2020":[-0.074181,-0.037179,0.061561,0.505759,0.431432,-0.421764,-0.666403,-0.372655],
                       "2021":[0.046049,-0.003487,0.11177,0.4844,0.384406,-0.605235,-0.727698,-0.303374]
                       },
                       index = [
                                "North",
                                "Northeast",
                                "East",
                                "Southeast",
                                "South",
                                "Southwest",
                                "West",
                                'Northwest'])

plt.rc('axes', labelsize=15,  titlesize=20) 
df_Asp.plot(kind="bar")

plt.title("Aspect and Glacier Retreat association")
plt.xlabel("Aspect class")
plt.xticks(rotation=0)
plt.ylabel("Weight of Evidence (WofE)")
plt.show()

