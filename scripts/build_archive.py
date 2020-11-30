import os
import datetime
import json
import arcpy
import MDCS

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

## Edit these paramters
workspace = '/data/sharedData/IMERGHHE/2019'#'//dannyk.esri.com/theShare/mrf-archive-2019'
config = '/data/sharedData/mdcs-py/Parameter/Config/gpm.xml'#'C:/PROJECTS/NASA/mdcs-py/Parameter/Config/gpm.xml'
mastermd = '/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019'#'//dannyk.esri.com/theShare/mrf-archive-2019/Master.gdb/GPM_2019'
outputsrcFC = '/data/sharedData/mdcs-py/0MD/inputtable.gdb/gpm_2019'#'//dannyk.esri.com/theShare/mrf-archive-2019/inputtable.gdb/gpm_2019'
outputsrcGDB = os.path.dirname(outputsrcFC)
interval = '30'
intervalunits = 'minutes'
bucket = '#'
infolder = '#'
startslice = '0'
endslice = '48'

total_start = datetime.datetime.now()

walk = arcpy.da.Walk(workspace, topdown=True, datatype="RasterDataset")

for dirpath, dirnames, filenames in walk:
    if len(filenames) > 0:
        start = datetime.datetime.now()
        filename = filenames[0]
        inputmrf = os.path.join(dirpath, filename)

        for root, dirs, files in os.walk(dirpath):
            for file in files:
                if file.endswith(".json"):
                    print(file)
                    with open(os.path.join(dirpath, file)) as f:
                        date_config = json.load(f)
                        startdate = replace_str_index(
                            date_config[str(int(startslice))], 10, "T").replace("-", "/")+".00"
                        enddate = replace_str_index(
                            date_config[str(int(endslice)-1)], 10, "T").replace("-", "/")+".00"
                        print(startdate)
                        print(enddate)
                        MDCS.main(14,
                              ['-i:' + config,
                              '-p:' + inputmrf + '$inmrf',
                              '-p:' + outputsrcFC + '$outFC',
                              '-p:' + startdate + '$sdate',
                              '-p:' + enddate + '$edate',
                              '-p:' + interval + '$interval',
                              '-p:' + intervalunits + '$intervalunits',
                              '-p:' + bucket + '$bucket',
                              '-p:' + infolder + '$infolder',
                              '-p:' + startslice + '$sslice',
                              '-p:' + endslice + '$eslice',
                              '-m:' + mastermd,
                              '-s:' + outputsrcFC,
                              '-c:buildSRCTable']) #+CM+RI+AR+SS+AI+SP

        finish = datetime.datetime.now()
        #print(f"finish: {finish}, runtime: {finish - start} ")

MDCS.main(4,
              ['-i:' + config,
              '-m:' + mastermd,
              '-s:' + outputsrcFC,
              '-c:CM+AR+SS+AI+SP']) #+RI

arcpy.Delete_management(outputsrcGDB)

total_finish = datetime.datetime.now()
#print(f"finish: {total_finish}, runtime: {total_finish - total_start} ")