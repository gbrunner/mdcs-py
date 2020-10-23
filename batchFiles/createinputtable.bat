rem The batch file will generate the source table with required fields and build the Mosaic dataset
set inputmrf=c:\data\Projects\gpm\multi_mrf\GPM_3IMERGHHE_V06B_201907_08.mrf
set outputsrcFC=c:\Image_Mgmt_Workflows\GPM\0MD\inputtable.gdb\gpm_data_daily
rem startdate and enddate has to be in the below format. ( YYYY/MM/DDTHH:MM:S.MS)
set startdate=2019/11/12T01:00:00.00
set enddate=2019/11/12T10:00:00.00
set interval=30
rem inervalunits can have only these values : months/weeks/days/hours/minutes/seconds
set intervalunits=minutes
set bucket=#
set infolder=#
set startslice=1
set endslice=5
rem buildinput source table
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" c:\Image_mgmt_Workflows\GPM\scripts\MDCS.py -i:c:\Image_mgmt_Workflows\GPM\Parameter\Config\gpm.xml -p:%inputmrf%$inmrf -p:%outputsrcFC%$outFC -p:%startdate%$sdate -p:%enddate%$edate -p:%interval%$interval -p:%intervalunits%$intervalunits -p:%bucket%$bucket -p:%infolder%$infolder -p:%startslice%$sslice -p:%endslice%$eslice -s:%outputsrcFC% -c:buildSRCTable