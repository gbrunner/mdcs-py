import arcpy
import os
#mosaic = r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM_2019'  # input("Enter full path to an object : ")
#arcpy.env.workspace = '/data/sharedData/mdcs-py/Parameter/RasterFunctionTemplates'

mosaic = r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM_2019'#'Z:/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019'
rft = r'C:\PROJECTS\NASA\mdcs-py\Parameter\RasterFunctionTemplates\GPM_Stretch.rft.xml'#'Z:/data/sharedData/mdcs-py/Parameter/RasterFunctionTemplates/GPM_Stretch.rft.xml'
print(mosaic)
print(arcpy.Exists(mosaic))
print(rft)
print(os.path.isfile(rft))


#arcpy.management.SetMosaicDatasetProperties(r"C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM_2019", 5000, 5000, "LERC;JPEG;NONE;LZ77", "LERC", 80, 0.001, "BILINEAR", "CLIP", "FOOTPRINTS_DO_NOT_CONTAIN_NODATA", "NOT_CLIP", "NOT_APPLY", "Basic", "Basic", "ByAttribute;Center;NorthWest;Nadir;LockRaster;Seamline;None", "ByAttribute", '', "2050/01/01", "ASCENDING", "FIRST", 10, 300, 300, 1, 0.8, "0 0", "BASIC", "Name;MinPS;MaxPS;LowPS;HighPS;GroupName;ProductName;Variable;StdTime;Dimensions;StdTime", "ENABLED", "StdTime", "StdTime", '', None, 20, 1000, "GENERIC", 1, "GPM_Stretch_StdDev_Colormap;GPM_Stretch_DRA;C:/PROJECTS/NASA/mdcs-py/Parameter/RasterFunctionTemplates/GPM_Stretch.rft.xml", "None", None, '', "NONE", None)


def scrapeMosaicMetadata(fq_path):
    descObj = arcpy.Describe(fq_path)
    descObjType = descObj.dataType
    props = {}
    props['Mosaic_Dataset_props'] = ['allowedCompressionMethods', 'allowedFields', 'allowedMensurationCapabilities',
                                     'allowedMosaicMethods',
                                     'applyColorCorrection', 'blendWidth', 'blendWidthUnits', 'cellSizeToleranceFactor',
                                     'childrenNames', 'clipToBoundary', 'clipToFootprint',
                                     'defaultCompressionMethod', 'defaultMensurationCapability', 'defaultMosaicMethod',
                                     'defaultProcessingTemplate',
                                     'defaultResamplingMethod', 'dimensionAttributes', 'dimensionNames',
                                     'dimensionValues', 'endTimeField',
                                     'footprintMayContainNoData', 'GCSTransforms', 'isMultidimensional', 'JPEGQuality',
                                     'LERCTolerance',
                                     'maxDownloadImageCount', 'maxDownloadSizeLimit', 'maxRastersPerMosaic',
                                     'maxRecordsReturned', 'maxRequestSizeX',
                                     'maxRequestSizeY', 'minimumPixelContribution', 'mosaicOperator',
                                     'multidimensionalInfo', 'orderBaseValue',
                                     'orderField', 'processingTemplates', 'rasterMetadataLevel', 'referenced',
                                     'sortAscending', 'startTimeField',
                                     'timeValueFormat', 'useTime', 'variableAttributes', 'variableNames',
                                     'viewpointSpacingX', 'viewpointSpacingY']

    metadata = {}
    for propGroup in props:
        for prop in props[propGroup]:
            try:
                value = getattr(descObj, prop)
                metadata.update({propGroup + ': ' + prop: value})
            except:
                pass
    # print(type(metadata))
    return metadata

print("Adding raster function template.")
arcpy.EditRasterFunction_management(mosaic,
                                    "EDIT_MOSAIC_DATASET",
                                    "INSERT",
                                    rft,
                                    'GPM_Stretch')
print("Added raster function.")

objMetaDict = scrapeMosaicMetadata(mosaic)
for attribute, value in objMetaDict.items():
    print('{} : {}'.format(attribute, value))