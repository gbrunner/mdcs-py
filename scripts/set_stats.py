import os
import datetime
import json
import arcpy
import MDCS

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

## Edit these paramters
#workspace ='/arcgis-dev-mosaic-share/IMERGHHE/2019'#'//dannyk.esri.com/theShare/mrf-archive-2019'
config = 'C:/PROJECTS/NASA/mdcs-py/Parameter/Config/gpm.xml'#'/arcgis-dev-mosaic-share/mdcs-py/Parameter/Config/gpm.xml'#'C:/PROJECTS/NASA/mdcs-py/Parameter/Config/gpm.xml'
mastermd = r'C:\PROJECTS\NASA\0MD\Master.gdb\GPM_2019'#'/arcgis-dev-mosaic-share/mdcs-py/0MD/Master.gdb/GPM_2019'#'//dannyk.esri.com/theShare/mrf-archive-2019/Master.gdb/GPM_2019'
#outputsrcFC = '/arcgis-dev-mosaic-share/mdcs-py/0MD/inputtable.gdb/gpm_2019'#'//dannyk.esri.com/theShare/mrf-archive-2019/inputtable.gdb/gpm_2019'
#outputsrcGDB = os.path.dirname(outputsrcFC)
#interval = '30'
#intervalunits = 'minutes'
#bucket = '#'
#infolder = '#'
#startslice = '0'
#endslice = '48'

total_start = datetime.datetime.now()
print(total_start)


MDCS.main(3,
              ['-i:' + config,
              '-m:' + mastermd,
              '-c:SS']) #+RI
#CM+AR+SS+AI+

#arcpy.Delete_management(outputsrcGDB)

total_finish = datetime.datetime.now()
#print(f"finish: {total_finish}, runtime: {total_finish - total_start} ")