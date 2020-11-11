import arcpy

arcpy.AddRastersToMosaicDataset_management(in_mosaic_dataset="/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019",
                                           raster_type="Table",
                                           input_path="/data/sharedData/mdcs-py/0MD/inputtable.gdb/gpm_2019",
                                           update_cellsize_ranges="UPDATE_CELL_SIZES",
                                           update_boundary="UPDATE_BOUNDARY",
                                           update_overviews="NO_OVERVIEWS",
                                           maximum_pyramid_levels="",
                                           maximum_cell_size="0",
                                           minimum_dimension="1500",
                                           spatial_reference="",
                                           filter="#",
                                           sub_folder="SUBFOLDERS",
                                           duplicate_items_action="ALLOW_DUPLICATES",
                                           build_pyramids="NO_PYRAMIDS",
                                           calculate_statistics="NO_STATISTICS",
                                           build_thumbnails="NO_THUMBNAILS",
                                           operation_description="#",
                                           force_spatial_reference="NO_FORCE_SPATIAL_REFERENCE",
                                           estimate_statistics="NO_STATISTICS",
                                           aux_inputs="")