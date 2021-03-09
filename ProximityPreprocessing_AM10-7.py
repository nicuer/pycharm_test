# import modules
import arcpy
import arcpy.mapping as mapping

import datetime

# Set Overwrite Option and Clear Memory of any Existing Temporary Datasets
arcpy.env.overwriteOutput = True
arcpy.Delete_management("in_memory")

var_TimeDateFormat1 = '%d-%m-%Y %H:%M:%S'
var_TimeDateFormat2 = '%Y%m%d_%H%M'
str_DateTime = str(datetime.datetime.now().strftime(var_TimeDateFormat1))

var_Par0 = arcpy.GetParameterAsText(0) # TRP Layer
path_PA_GDB = arcpy.GetParameterAsText(1) + '\\' # Location of ProximityBaseDate.gdb
path_CSDL_GDB = arcpy.GetParameterAsText(2) + '\\' # r'C:\Data\CSDL on C\\' #  Locaiton of CSDL
path_RB_GDB = arcpy.GetParameterAsText(2) + '\\'  #  Locaiton of regional_business.gdb
var_Par3 = arcpy.GetParameterAsText(4) # process buffers or just updated buffer query layers
#var_Par4 = arcpy.GetParameterAsText(5) # update Rainforest Data
RainforAnalysis = True
RainforSigAnalysis = True
MOGAnalysis = True
GeologyAnalysis = True
SlopeClassAnalysis = True

# var_Par5 = arcpy.GetParameterAsText(5) # process buffers or just updated buffer query layers
# var_Par6 = arcpy.GetParameterAsText(6) # process buffers or just updated buffer query layers

# Check TRP (or a layer) has been set by user in form, otherwise exit file exists before proceeding
if len(var_Par0) <= 0: # first check TRP file exists before proceeding
    arcpy.AddMessage("** Stopping. No TRP set, this needs to be set in the first option of the form. " + str_DateTime)
    exit()



# fc_In = r'C:\Data\ArcGIS\Default1.gdb\fc_TRPTest'
# fc_OutA = r'C:\Data\ArcGIS\Default1.gdb\TRP_Buffer20'
 # get output locations for TRP buffers
fc_TRP = var_Par0
#fc_TRP = path_PA_GDB + "\\TRP"
fc_TRP20 = path_PA_GDB + "TRP_20"
fc_TRP50 = path_PA_GDB + "TRP_50"
fc_TRP100 = path_PA_GDB + "TRP_100"
fc_TRP250 = path_PA_GDB + "TRP_250"

arcpy.AddMessage('var_Par0: ' + var_Par0 + " - fc_TRP: " + fc_TRP + ' - fc_TRP50: ' + fc_TRP50)

# out_coor_system = "PROJCS['GDA2020_Vicgrid',GEOGCS['GDA2020',DATUM['GDA2020',SPHEROID['GRS_1980',6378137.0,298.257222101]]," \
#                 "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic']," \
#                 "PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',2500000.0],PARAMETER['Central_Meridian',145.0]," \
#                 "PARAMETER['Standard_Parallel_1',-36.0],PARAMETER['Standard_Parallel_2',-38.0],PARAMETER['Latitude_Of_Origin',-37.0],UNIT['Meter',1.0]]"
# transform_method = ["GDA_1994_To_GDA2020_1"]
# in_coor_system = "PROJCS['GDA_1994_VICGRID94',GEOGCS['GCS_GDA_1994',DATUM['D_GDA_1994',SPHEROID['GRS_1980',6378137.0,298.257222101]]," \
#                "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic']," \
#                "PARAMETER['False_Easting',2500000.0],PARAMETER['False_Northing',2500000.0],PARAMETER['Central_Meridian',145.0]," \
#                "PARAMETER['Standard_Parallel_1',-36.0],PARAMETER['Standard_Parallel_2',-38.0],PARAMETER['Latitude_Of_Origin',-37.0],UNIT['Meter',1.0]]",
# preserve_shape = "NO_PRESERVE_SHAPE",
# max_deviation ="",
# vertical ="NO_VERTICAL"

# get the map document 'CURRENT'
#mxd = mapping.MapDocument("CURRENT")
mxd = arcpy.mp.ArcGISProject("CURRENT")

# get the first data frame
#df = mapping.ListDataFrames(mxd, "*")[0]
#df = mapping.ListDataFrames(mxd)[0]
#df = mp.ListElements(mxd)[0]
df = mxd.listMaps("Map2")[0]

join_attributes = "ALL"
cluster_tolerance = ""
output_type = "INPUT"

# for lyr in df.listLayers():
#     if lyr.supports("SHOWLABELS"):
#        lblClasses = lyr.listLabelClasses()

if var_Par3:

    arcpy.AddMessage('\n1. Starting buffer creation analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    # create gdb to store outputs
    # out_GDB = 'TRP_ProximityAnalysisBaseData_TEST_' + str(datetime.datetime.now().strftime(var_TimeDateFormat2)) # TODO: Check if GDB already exists
    # arcpy.CreateFileGDB_management(fc_In, out_GDB, "10.0")

    # set buffer distances
    distance_Buffer20 = "20 Meters"
    distance_Buffer50 = "50 Meters"
    distance_Buffer100 = "100 Meters"
    distance_Buffer250 = "250 Meters"

    # Process buffers (20, 50, 100, 250m
    arcpy.AddMessage("** 1. Creating buffers")
    arcpy.analysis.Buffer(var_Par0, fc_TRP20, distance_Buffer20, "OUTSIDE_ONLY", "ROUND", "NONE", "","GEODESIC") #TODO: GEODESIC or PLANAR?
    arcpy.analysis.Buffer(var_Par0, fc_TRP50, distance_Buffer50, "OUTSIDE_ONLY", "ROUND", "NONE", "", "GEODESIC")
    arcpy.analysis.Buffer(var_Par0, fc_TRP100, distance_Buffer100, "OUTSIDE_ONLY", "ROUND", "NONE", "", "GEODESIC")
    arcpy.analysis.Buffer(var_Par0, fc_TRP250, distance_Buffer250, "OUTSIDE_ONLY", "ROUND", "NONE", "", "GEODESIC")

if RainforAnalysis:
    arcpy.AddMessage('\n2. Starting Rainfor analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    fc_Rainfor = path_CSDL_GDB + 'FORESTS.gdb\\RAINFOR'

    # Process: Clip (Clip) (analysis)
    fc_RAINFOR_TRP_Clip = path_PA_GDB + "z_RAINFOR_TRP_Clip"
    fc_RAINFOR_TRP50_Clip = path_PA_GDB + "z_RAINFOR_TRP50_Clip"
    arcpy.analysis.Clip(fc_Rainfor, fc_TRP, fc_RAINFOR_TRP_Clip, cluster_tolerance)
    arcpy.analysis.Clip(fc_Rainfor, fc_TRP50, fc_RAINFOR_TRP50_Clip, cluster_tolerance)

    # Process: Intersect (Intersect) (analysis)
    fc_RAINFOR_TRP_Intersect = path_PA_GDB + "\\z_RAINFOR_TRP_Intersect"
    fc_RAINFOR_TRP50_Intersect = path_PA_GDB + "\\z_RAINFOR_TRP50_Intersect"
    arcpy.analysis.Intersect([fc_RAINFOR_TRP_Clip, fc_TRP], fc_RAINFOR_TRP_Intersect, join_attributes, cluster_tolerance, output_type)
    arcpy.analysis.Intersect([fc_RAINFOR_TRP50_Clip, fc_TRP50], fc_RAINFOR_TRP50_Intersect, join_attributes, cluster_tolerance, output_type)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    fc_RAINFOR_TRP = path_PA_GDB + "\\hRAINFOR_TRP"
    fc_RAINFOR_TRP50 = path_PA_GDB + "\\hRAINFOR_TRP50"
    arcpy.management.MultipartToSinglepart(fc_RAINFOR_TRP_Intersect, fc_RAINFOR_TRP)
    arcpy.management.MultipartToSinglepart(fc_RAINFOR_TRP50_Intersect, fc_RAINFOR_TRP50)

    # Remove unwanted fields and update Area (ha)
    fields_Rainfor = ('ENUM_ID_13','EVC_RF', 'COUPE')
    for layer in [fc_RAINFOR_TRP, fc_RAINFOR_TRP50]:

        for f in arcpy.ListFields(layer):
            if f.name not in fields_Rainfor:
                try:
                   arcpy.DeleteField_management(layer, f)
                except:
                    print
                    arcpy.GetMessages()
        arcpy.AddField_management(layer, "Area_ha", "DOUBLE", 9, 2, "", "Area (ha)", "NULLABLE","NON_REQUIRED", "")
        arcpy.management.CalculateField(layer, "Area_ha", "!SHAPE.AREA@HECTARES!", "PYTHON3")

if RainforSigAnalysis:
    arcpy.AddMessage('\n2. Starting Rainfor analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    fc_RainforSig = path_CSDL_GDB + 'FLORAFAUNA1.GDB\\RFSOS100'

    # Process: Clip (Clip) (analysis)
    fc_RAINFORSIG_TRP_Clip = path_PA_GDB + "z_RAINFORSIG_TRP_Clip"
    fc_RAINFORSIG_TRP100_Clip = path_PA_GDB + "z_RAINFORSIG_TRP100_Clip"
    arcpy.analysis.Clip(fc_RainforSig, fc_TRP, fc_RAINFORSIG_TRP_Clip, cluster_tolerance)
    arcpy.analysis.Clip(fc_RainforSig, fc_TRP100, fc_RAINFORSIG_TRP100_Clip, cluster_tolerance)

    # Process: Intersect (Intersect) (analysis)
    fc_RAINFORSIG_TRP_Intersect = path_PA_GDB + "\\z_RAINFORSIG_TRP_Intersect"
    fc_RAINFORSIG_TRP100_Intersect = path_PA_GDB + "\\z_RAINFORSIG_TRP100_Intersect"
    arcpy.analysis.Intersect([fc_RAINFORSIG_TRP_Clip, fc_TRP], fc_RAINFORSIG_TRP_Intersect, join_attributes, cluster_tolerance, output_type)
    arcpy.analysis.Intersect([fc_RAINFORSIG_TRP100_Clip, fc_TRP100], fc_RAINFORSIG_TRP100_Intersect, join_attributes, cluster_tolerance, output_type)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    fc_RAINFORSIG_TRP = path_PA_GDB + "\\hRAINFORSIG_TRP"
    fc_RAINFORSIG_TRP100 = path_PA_GDB + "\\hRAINFORSIG_TRP100"
    arcpy.management.MultipartToSinglepart(fc_RAINFORSIG_TRP_Intersect, fc_RAINFORSIG_TRP)
    arcpy.management.MultipartToSinglepart(fc_RAINFORSIG_TRP100_Intersect, fc_RAINFORSIG_TRP100)

    # Remove unwanted fields and update Area (ha)
    fields_Rainfor = ('ENUM_ID_13','EVC_RF', 'COUPE')
    for layer in [fc_RAINFORSIG_TRP, fc_RAINFORSIG_TRP100]:

        for f in arcpy.ListFields(layer):
            if f.name not in fields_Rainfor:
                try:
                   arcpy.DeleteField_management(layer, f)
                except:
                    print
                    arcpy.GetMessages()
        arcpy.AddField_management(layer, "Area_ha", "DOUBLE", 9, 2, "", "Area (ha)", "NULLABLE","NON_REQUIRED", "")
        arcpy.management.CalculateField(layer, "Area_ha", "!SHAPE.AREA@HECTARES!", "PYTHON3")

if MOGAnalysis:
    arcpy.AddMessage('\n3. Starting MOG analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    fc_MOG = path_CSDL_GDB + 'FORESTS.GDB\\MOG2009'

    # Process: Select (Select) (analysis)
    fc_MOG_TRP_Select = path_PA_GDB + "z_MOG2009_TRP_Select"
    arcpy.analysis.Select(fc_MOG, fc_MOG_TRP_Select, where_clause="X_OGCODE = 'Old Growth Forest'")
    
    # Process: Clip (Clip) (analysis)
    fc_MOG_TRP_Clip = path_PA_GDB + "z_MOG009_TRP_Clip"
    #fc_MOG_TRP50_Clip = path_PA_GDB + "z_MOG_TRP50_Clip"
    arcpy.analysis.Clip(fc_MOG_TRP_Select, fc_TRP, fc_MOG_TRP_Clip, cluster_tolerance)
    #arcpy.analysis.Clip(fc_MOG_TRP_Select, fc_TRP50, fc_MOG_TRP50_Clip, cluster_tolerance)

    # Process: Intersect (Intersect) (analysis)
    fc_MOG_TRP_Intersect = path_PA_GDB + "\\z_MOG2009_TRP_Intersect"
    #fc_MOG_TRP50_Intersect = path_PA_GDB + "\\z_MOG_TRP50_Intersect"
    arcpy.analysis.Intersect([fc_MOG_TRP_Clip, fc_TRP], fc_MOG_TRP_Intersect, join_attributes,
                             cluster_tolerance, output_type)
    #arcpy.analysis.Intersect([fc_MOG_TRP50_Clip, fc_TRP50], fc_MOG_TRP50_Intersect, join_attributes, cluster_tolerance, output_type)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    fc_MOG_TRP = path_PA_GDB + "\\aMOG2009_TRP"
    #fc_MOG_TRP50 = path_PA_GDB + "\\aMOG_TRP50"
    arcpy.management.MultipartToSinglepart(fc_MOG_TRP_Intersect, fc_MOG_TRP)
    #arcpy.management.MultipartToSinglepart(fc_MOG_TRP50_Intersect, fc_MOG_TRP50)

    # Remove unwanted fields and update Area (ha)
    fields_Rainfor = ('OGCODE', 'X_OGCODE', 'COUPE')
    for layer in [fc_MOG_TRP]:

        for f in arcpy.ListFields(layer):
            if f.name not in fields_Rainfor:
                try:
                    arcpy.DeleteField_management(layer, f)
                except:
                    print
                    arcpy.GetMessages()
        arcpy.AddField_management(layer, "Area_ha", "DOUBLE", 9, 2, "", "Area (ha)", "NULLABLE", "NON_REQUIRED", "")
        arcpy.management.CalculateField(layer, "Area_ha", "!SHAPE.AREA@HECTARES!", "PYTHON3")

if GeologyAnalysis:
    arcpy.AddMessage('\n5. Starting Geology analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    fc_GEOL = path_CSDL_GDB + 'MINERALS.GDB\SG_GEOLOGICAL_UNIT_250K'


    # Process: Select (Select) (analysis)
    fc_GEOL_TRP_Select = path_PA_GDB + "z_GEOL_TRP_Select"
    arcpy.analysis.Select(fc_GEOL, fc_GEOL_TRP_Select, where_clause="LITHOLOGY LIKE '%granit%'")

    # Process: Clip (Clip) (analysis)
    fc_GEOL_TRP_Clip = path_PA_GDB + "z_GEOL_TRP_Clip"
    arcpy.analysis.Clip(fc_GEOL_TRP_Select, fc_TRP, fc_GEOL_TRP_Clip, cluster_tolerance)

    # Process: Intersect (Intersect) (analysis)
    fc_GEOL_TRP_Intersect = path_PA_GDB + "\\z_GEOL_TRP_Intersect"
    arcpy.analysis.Intersect([fc_GEOL_TRP_Clip, fc_TRP], fc_GEOL_TRP_Intersect, join_attributes, cluster_tolerance, output_type)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    fc_GEOL_TRP = path_PA_GDB + "\\aGEOL_GRANITE_TRP"
    arcpy.management.MultipartToSinglepart(fc_GEOL_TRP_Intersect, fc_GEOL_TRP)

    # Remove unwanted fields and update Area (ha)
    fields_Rainfor = ('LITHOLOGY', 'ID', 'DESCRIPTION','POSITIONALACCURACY','COUPE')
    for layer in [fc_GEOL_TRP]:

        for f in arcpy.ListFields(layer):
            if f.name not in fields_Rainfor:
                try:
                    arcpy.DeleteField_management(layer, f)
                except:
                    print
                    arcpy.GetMessages()
        arcpy.AddField_management(layer, "Area_ha", "DOUBLE", 9, 2, "", "Area (ha)", "NULLABLE", "NON_REQUIRED", "")
        arcpy.management.CalculateField(layer, "Area_ha", "!SHAPE.AREA@HECTARES!", "PYTHON3")

if SlopeClassAnalysis:
    arcpy.AddMessage('\n5. Starting Slope Class analysis ' + str_DateTime + ' *** TESTING VERSION ONLY ***')

    fc_RainforSig = path_RB_GDB + 'regional_business.gdb\\BLD_SLOPECLASS_DEG'

    # Process: Clip (Clip) (analysis)
    fc_SLOPE_TRP_Clip = path_PA_GDB + "z_SLOPE_TRP_Clip"
    arcpy.analysis.Clip(fc_RainforSig, fc_TRP, fc_SLOPE_TRP_Clip, cluster_tolerance)

    # Process: Intersect (Intersect) (analysis)
    fc_SLOPE_TRP_Intersect = path_PA_GDB + "\\z_SLOPE_TRP_Intersect"
    arcpy.analysis.Intersect([fc_SLOPE_TRP_Clip, fc_TRP], fc_SLOPE_TRP_Intersect, join_attributes, cluster_tolerance, output_type)

    # Process: Multipart To Singlepart (Multipart To Singlepart) (management)
    fc_SLOPE_TRP = path_PA_GDB + "\\hSLOPE_TRP"
    arcpy.management.MultipartToSinglepart(fc_SLOPE_TRP_Intersect, fc_SLOPE_TRP)

    # Remove unwanted fields and update Area (ha)
    fields_Rainfor = ('CLASS','COUPE')
    for layer in [fc_SLOPE_TRP]:

        for f in arcpy.ListFields(layer):
            if f.name not in fields_Rainfor:
                try:
                   arcpy.DeleteField_management(layer, f)
                except:
                    print
                    arcpy.GetMessages()
        arcpy.AddField_management(layer, "Area_ha", "DOUBLE", 9, 2, "", "Area (ha)", "NULLABLE","NON_REQUIRED", "")
        arcpy.AddField_management(layer, "CoupeSlope", "TEXT", "", "", 30, "CoupeID SlopeClass", "NULLABLE", "NON_REQUIRED", "")
        arcpy.management.CalculateField(layer, "Area_ha", "!SHAPE.AREA@HECTARES!", "PYTHON3")
        arcpy.management.CalculateField(layer, "CoupeSlope", "!SHAPE.AREA@HECTARES!", "PYTHON3")
# add data to map
# name buffer layer in data frame
# lyr_NewName = os.path.basename(fc_In)
# lyr_NewName = (lyr_NewName[:(len(lyr_NewName) -0)])
# fc_Buffer20.name = "TRP 20m Buffer"
# fc_Buffer50.name = "TRP 50m Buffer"
# fc_Buffer100.name = "TRP 200m Buffer"
# fc_Buffer250.name = "TRP 250m Buffer"
#
# # zoom to layer extent of largest buffer area #TODO: If not working put below #add the layers to the map
# lyr_extent = fc_Buffer250.getExtent(True)
# # lyr_extent = fc_Buffer20.getExtent(True)
# df.extent = lyr_extent

# add the layers to the map at the top of the TOC in data frame 0
# mapping.AddLayer(df, fc_Buffer20, "TOP")
# mapping.AddLayer(df, fc_Buffer50, "TOP")
# mapping.AddLayer(df, fc_Buffer100, "TOP")
# mapping.AddLayer(df, fc_Buffer250, "TOP")

# update symbology
# arcpy.AddMessage("** 5. Applying Symbology")
# str_SymPath = r'C:\Users\nb14\OneDrive - Department of Environment, Land, Water and Planning\OCR\Projects\Proximity Analysis\Symbology' #TODO: Move symbols to location where tool will be packaged location
# updateLayer = mapping.ListLayers(mxd, fc_Buffer20.name, df)[0]
# sourceLayer = mapping.Layer(str_SymPath + '\TRP_A.lyr')
# mapping.UpdateLayer(df, updateLayer, sourceLayer, True)
# updateLayer = mapping.ListLayers(mxd, fc_Buffer50.name, df)[0]
# sourceLayer = mapping.Layer(str_SymPath + '\TRP_B.lyr')
# mapping.UpdateLayer(df, updateLayer, sourceLayer, True)
# updateLayer = mapping.ListLayers(mxd, fc_Buffer100.name, df)[0]
# sourceLayer = mapping.Layer(str_SymPath + '\TRP_C.lyr')
# mapping.UpdateLayer(df, updateLayer, sourceLayer, True)
# updateLayer = mapping.ListLayers(mxd, fc_Buffer250.name, df)[0]
# sourceLayer = mapping.Layer(str_SymPath + '\TRP_D.lyr')
# mapping.UpdateLayer(df, updateLayer, sourceLayer, True)

# refresh PA GDB