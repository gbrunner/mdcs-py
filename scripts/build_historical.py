import os
import MDCS
import arcpy

arcpy.env.workspace = r'D:\DATA\NSA_MRF\inputMRFData\GPM\GPM_3IMERGHHE06B\FourMonthly'
mrf_list = arcpy.ListRasters()

raster_year_month = []

mastermd=r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM'
outputsrcFC=r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\inputtable.gdb\gpm_data_daily'
interval='30'
intervalunits='minutes'
bucket='#'
infolder='#'
startslice='1'

for raster in mrf_list:
    date_string = raster.split("_")[2]
    year = date_string[0:4]
    month = date_string[4:6]
    year_int = int(date_string[0:4])
    month_int = int(date_string[4:6])
    if year == '2000':
        print("Pass on these")
        raster_year_month.append([raster, year, month])
    else:
        if year in ['2004', '2008', '2012']:
            if month == '01':
                #raster_year_month.append([raster, year, month])
                startdate = '2007/01/01T00:00:00.00'
                enddate = '2007/04/30T23:30:00.00'
                endslice = '5808'
        else:
            if month == '01':
                startdate = year+'/01/01T00:00:00.00'
                enddate = year+'/04/30T23:30:00.00'
                endslice = '5760'

            if month == '05':
                startdate = year+'/05/01T00:00:00.00'
                enddate = year+'/08/30T23:30:00.00'
                endslice = '5904'

            if month == '09':
                startdate = year+'/09/01T00:00:00.00'
                enddate = year+'/12/30T23:30:00.00'
                endslice = '5856'


        inputmrf = os.path.join(arcpy.env.workspace, raster)

        MDCS.main(14,
              ['-i:C:/PROJECTS/NASA/gpm-newmdcs/Parameter/Config/gpm.xml',
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
              '-c:buildSRCTable+CM+RI+AR+SS+AI+SP'])