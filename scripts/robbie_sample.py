def Strip_Ext(mpath):
    footprint = "Footprint"
    fieldname = "ImageURL"
    extensions = ['tif', 'TIF', 'Tif', 'tIf', 'tiF', 'TIf', 'TiF', 'tIF']

    for dirpath, dirnames, filenames in arcpy.da.Walk(mpath, topdown=True, datatype=['MosaicDataset']):
        for filename in filenames:
            mlayer_name = '{}_md'.format(filename)
            mlayer = arcpy.MakeMosaicLayer_management(os.path.join(dirpath, filename), mlayer_name)

            footprints = os.path.join(mlayer_name, footprint)
            flayer = footprints

            field = findfield(footprints, fieldname)
            if field:
                # Replace upper, lower and mixed case versions of the extension tif
                for extension in extensions:
                    expression = "!{}!.replace(\".{}\", \"\", -1)".format(fieldname, extension)
                    arcpy.AddMessage(
                        'About to strip {} extension for field {} in mosaic {}'.format(extension, field.name, filename))
                    arcpy.CalculateField_management(flayer, fieldname, expression, "PYTHON")