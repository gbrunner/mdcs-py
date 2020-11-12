import sys
import datetime
import MDCS
import os

def main():

    ## Edit these paramters
    raster = sys.argv[1] #'D:/DATA/NASA_DAILY/mrf-archive-2019/2019/001/2019-001-z48.mrf'
    #raster = 'D:/DATA/NASA_DAILY/mrf-archive-2019/2019/001/2019-001-z48.mrf'
    config = 'C:/PROJECTS/NASA/mdcs-py/Parameter/Config/gpm.xml'
    mastermd = 'C:/PROJECTS/NASA/gpm-newmdcs/0MD/Master.gdb/GPM_2019_001_z48'
    outputsrcFC = 'C:/PROJECTS/NASA/gpm-newmdcs/0MD/inputtable.gdb/gpm_2019_001_z48'
    interval = '30'
    intervalunits = 'minutes'
    bucket = '#'
    infolder = '#'
    startslice = '0'
    endslice = '47'

    raster_name = os.path.basename(raster)

    date_info = raster_name.split("-")
    year = date_info[0]
    month_day = date_info[1]
    year_int = int(year)
    day_of_year = int(month_day)
    d = datetime.date(year_int, 1, 1) + datetime.timedelta(day_of_year - 1)
    month = str(d.month)
    day = str(d.day)

    startdate = year + '/' + month + '/' + day + 'T00:00:00.00'
    enddate = year + '/' + month + '/' + day + 'T23:30:00.00'
    print(startdate)
    print(enddate)
    MDCS.main(14,
          ['-i:' + config,
          '-p:' + raster + '$inmrf',
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

if __name__ == '__main__':
    main()