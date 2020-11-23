import arcpy
print("adding raster function template.")
mosaic = '/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019'
rft = '/data/sharedData/mdcs-py/Parameter/RasterFunctionTemplates/GPM_Stretch.rft.xml'
arcpy.EditRasterFunction_management(mosaic,
                                    "EDIT_MOSAIC_DATASET",
                                    "INSERT",
                                    rft,
                                    '')
print("done.")
