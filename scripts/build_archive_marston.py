import os, sys
import datetime
import time
import json
import arcpy
import MDCS
import pdb

def doy_to_year_month_day(year, doy):
    year = int(year)
    dtg = str(datetime.datetime(year,1,1) + datetime.timedelta(int(doy) - 1)).split('-')
    day = int(dtg[2].split(' ')[0])
    month = int(dtg[1])
    starDate = '%04d/%02d/%02dT00:00:00.00' % (year, month, day)
    endDate = '%04d/%02d/%02dT23:30:00.00' % (year, month, day)
    return starDate,endDate

## Edit these paramters
testCase = 'mrf-archive-2019'
dataSrc = 'D:/DATA/NASA_DAILY'#'/data1/IMERGHHE'
mdcsSrc = 'C:/PROJECTS/NASA/mdcs-py'

workspace = '{}/{}'.format(dataSrc,testCase)
config = '{}/Parameter/Config/gpm.xml'.format(mdcsSrc)
mastermd = '{}/0MD/Master.gdb/GPM_2019'.format(mdcsSrc) 
outputsrcFC = '{}/0MD/inputtable.gdb/gpm_2019'.format(mdcsSrc)
interval = '30'
intervalunits = 'minutes'
bucket = '#'
infolder = '#'
startslice = '0'
endslice = '47'

years = os.listdir(workspace)
start_time = time.time()
for y in years:
    print('Processing years: ' + y)

print('Looping over years and doy in years...')

numberOfProcessedDoy = 0

if len(years) > 0:
    for year in years:
        print('Processing doys in ' + year)
        doys = os.listdir('%s/%s' % (workspace,year))
        if len(doys) > 0:
            for doy in doys:
                print('Processing files in %s/%s' % (year, doy))
                doyFiles = os.listdir('%s/%s/%s' % (workspace, year, doy))
                for f in doyFiles:
                    print('doyFile: ' + f)
                if len(doyFiles) > 0:
                    numberOfProcessedDoy += 1
                    inputmrf = '%s/%s/%s/%s-%s-z48.mrf' % (workspace, year, doy, year, doy)
                    print('inputmrf = ' + inputmrf)
                    startdate, enddate = doy_to_year_month_day(year, doy)
                    print('Start date and time: ' + startdate)
                    print('End date and time ' + enddate)
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
                               '-c:buildSRCTable'])

timeTaken1 = (time.time() - start_time)
print("Built tables in %s seconds" % timeTaken1)
start_time = time.time()
print('numberOfProcessedDoy = %d' % numberOfProcessedDoy)
#pdb.set_trace()

MDCS.main(4,
          ['-i:' + config,
           '-m:' + mastermd,
           '-s:' + outputsrcFC,
           '-c:CM+RI+AR+SS+AI+SP'])

timeTaken2 = (time.time() - start_time)
print("Built mosaic in %f seconds" % timeTaken2)
print("Total time = %f seconds" % (timeTaken2 + timeTaken1))
