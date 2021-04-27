import arcpy

#mosaic = r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM_2019'  # input("Enter full path to an object : ")
mosaic = "C:/PROJECTS/NASA/0MD/Master.gdb/GPM_2019"#'/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019'

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

objMetaDict = scrapeMosaicMetadata(mosaic)
for attribute, value in objMetaDict.items():
    print('{} : {}'.format(attribute, value))