import arcpy

fc = '/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019'
fields = ['Name', 'Tag', 'StdTime']

# For each row, print the WELL_ID and WELL_TYPE fields, and
# the feature's x,y coordinates
with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
        print(u'{0}, {1}, {2}'.format(row[0], row[1], row[2]))