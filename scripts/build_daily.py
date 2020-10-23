import MDCS


inputmrf=r'D:\DATA\NSA_MRF\inputMRFData\GPM\GPM_3IMERGHHE06B\FourMonthly\GPM_3IMERGHHE.V06B_20070101T0000.mrf'
outputsrcFC=r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\inputtable.gdb\gpm_data_daily'
##rem startdate and enddate has to be in the below format. ( YYYY/MM/DDTHH:MM:S.MS)
startdate='2007/01/01T00:00:00.00'
enddate='2007/04/30T23:30:00.00'
interval='30'
#inervalunits can have only these values : months/weeks/days/hours/minutes/seconds
intervalunits='minutes'
mastermd=r'C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM'
bucket='#'
infolder='#'
startslice='1'
endslice='5760'

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