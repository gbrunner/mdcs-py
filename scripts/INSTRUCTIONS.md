# Instructions for building the mosaic of all achived GPM MRF files

## Create OMD folder
1. In the mdcs-py folder, create a new folder named **0MD**.

## Set Paramters in build_archive.py
1. Change workspace to the location of the MRF files
```
workspace = 'D:/DATA/NASA_DAILY/mrf-archive-2019'
```
2. Point to your config file in /Parameter/Config/gpm.xml
```
config = 'C:/PROJECTS/NASA/gpm-newmdcs/Parameter/Config/gpm.xml'
```
3. Define the mosaic dataset that you will be creating. We recommend creating it in the **0MD** folder.
```
mastermd = 'C:/PROJECTS/NASA/gpm-newmdcs/0MD/Master.gdb/GPM_2019'
```
4. Define the table that you will create in order to populate the mosaic dataset. We recommend creating it in **0MD** folder.
```
outputsrcFC = 'C:/PROJECTS/NASA/gpm-newmdcs/0MD/inputtable.gdb/gpm_2019'
 ```

## Update parameters in Config/gpm.xml

1. Open **gpm.xml** in the **Config** folder.
2. Set ```<WorkspacePath>c:\PROJECTS\NASA\gpm-newmdcs\0MD</WorkspacePath>``` to point to the folder that will hold your mosaic dataset.
3. Set ```<Geodatabase>Master.gdb</Geodatabase>``` to the name of your output mosaic.
4. Set ```<processing_templates>C:\PROJECTS\NASA\gpm-newmdcs\Parameter\RasterFunctionTemplates\GPM_Stretch_DRA.rft.xml</processing_templates>``` to point to your **GPM_Stretch_DRA raster function**.
5. These should be the only changes you need to make.

## Update MDCS_UC.py

1. Open **MDCS_UC.py**.
2. Go to line 200. It will read:
```<DataFile>c:/mrfcache/gpm/{4}.mrf_cache</DataFile><IndexFile>c:/mrfcache/gpm/{4}.mrf_cache</IndexFile></Raster>\n' ```
3. Change **c:/mrfcache** to be a folder that exists on your system. We recommend that you create the **mrfcache** folder on your C, D, or Z drive.
4. Go to line 222: It will read:
```<DataFile>c:/mrfcache/gpm/{2}.mrf_cache</DataFile><IndexFile>c:/mrfcache/gpm/{2}.mrf_cache</IndexFile></Raster>\n'```
5. Again, change **c:/mrfcache** to be a folder that exists on your system. We recommend that you create the **mrfcache** folder on your C, D, or Z drive.

## Delete the *inputtable.gdb* after every run
The **inputtable.gdb** contains a feature class that is used to update the msoaic dataset. We want to insert only new records. Therefore, after every run, delete the **inputtable.gdb** using [**arcpy.Delete_management()](https://pro.arcgis.com/en/pro-app/tool-reference/data-management/delete.htm).

Add the following lines to each python script: 
1. ```import arcpy```
2. Define the source geodatabase: ```outputsrcGDB = 'C:/PROJECTS/NASA/gpm-newmdcs/0MD/inputtable.gdb'```
3. At the end of the process, delete ```outputsrcGDB``` using: ```arcpy.Delete_management(outputsrcGDB)```
