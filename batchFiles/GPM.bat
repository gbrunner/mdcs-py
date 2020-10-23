set outputsrcFC=c:\Image_Mgmt_Workflows\GPM\0MD\inputtable.gdb\gpm_data_daily
rem startdate and enddate has to be in the below format.
set mastermd=c:\Image_mgmt_Workflows\GPM\0MD\Master.gdb\GPM
rem build Mosaic
"c:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" c:\Image_mgmt_Workflows\GPM\scripts\MDCS.py -i:c:\Image_mgmt_Workflows\GPM\Parameter\Config\gpm.xml -m:%mastermd% -s:%outputsrcFC% -c:CM+AR+SP+SS+AI

