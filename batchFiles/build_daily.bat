rem The batch file will generate the source table with required fields and build the Mosaic dataset
set inputmrf=D:\DATA\NSA_MRF\inputMRFData\GPM\GPM_3IMERGHHE06B\FourMonthly\GPM_3IMERGHHE.V06B_20070101T0000.mrf
set outputsrcFC=C:\PROJECTS\NASA\gpm-newmdcs\0MD\inputtable.gdb\gpm_data_daily
rem startdate and enddate has to be in the below format. ( YYYY/MM/DDTHH:MM:S.MS)
set startdate=2007/01/01T00:30:00.00
set enddate=2007/04/30T23:30:00.00
set interval=30
rem inervalunits can have only these values : months/weeks/days/hours/minutes/seconds
set intervalunits=minutes
set mastermd=C:\PROJECTS\NASA\gpm-newmdcs\0MD\Master.gdb\GPM
set bucket=#
set infolder=#
set startslice=1
set endslice=5760
rem append records to the mosaic
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" C:\PROJECTS\NASA\gpm-newmdcs\scripts\MDCS.py -i:C:\PROJECTS\NASA\gpm-newmdcs\Parameter\Config\gpm.xml -p:%inputmrf%$inmrf -p:%outputsrcFC%$outFC -p:%startdate%$sdate -p:%enddate%$edate -p:%interval%$interval -p:%intervalunits%$intervalunits -p:%bucket%$bucket -p:%infolder%$infolder -p:%startslice%$sslice -p:%endslice%$eslice -m:%mastermd% -s:%outputsrcFC% -c:buildSRCTable+CM+RI+AR+SS+AI+SP