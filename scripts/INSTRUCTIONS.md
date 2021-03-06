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
The **inputtable.gdb** contains a feature class that is used to update the msoaic dataset. We want to insert only new records. Therefore, after every run, delete the **inputtable.gdb** using [**arcpy.Delete_management()**](https://pro.arcgis.com/en/pro-app/tool-reference/data-management/delete.htm).

Add the following lines to each python script, **build_archive.py** and **add_daily_to_archive.py**: 
1. ```import arcpy```
2. Define the source geodatabase: ```outputsrcGDB = os.path.dirname(outputsrcFC)```
3. At the end of the process, delete ```outputsrcGDB``` using: ```arcpy.Delete_management(outputsrcGDB)```


## Helper scripts
I have included two helper scripts to verify that MRF slides are being added to the mosaic and that the mosaic dataset properties are being updated.

1. [print_table.py](https://github.com/gbrunner/mdcs-py/blob/master/scripts/print_table.py) prints the list of specified mosaic dataset MRF slice properties ('Name', 'Tag', 'StdTime') to the screen to verify the slices have been added to the mosaic.
2. [check_mosaic_properties.py](https://github.com/gbrunner/mdcs-py/blob/master/scripts/check_mosaic_properties.py) checks that the properties of a mosaic have been updated.

# Publishing an image service through the ArcGIS Admin page

## Configure the image service JSON

1. In the *scripts* folder, you will see a file name [**image_service.json**](https://github.com/gbrunner/mdcs-py/blob/master/scripts/image_service.json).
2. Configure that file to work with your mosaic dataset and ArcGIS Server setup. Here are the following items you need to set or change in the JSON file:
  - "serviceName": "GPM_2019_Demo" - Name the service whatever you would like.
  - "description": "GPM data for 2019" - Give the service a better description than I have.
  - "cacheDir": "/data/sharedData/directories/arcgiscache" - Find the **arcgiscache** on your system. Set this to be the "cacheDir".
  - "path": "/data/sharedData/mdcs-py/0MD/Master.gdb/GPM_2019" - Set the "path" to be the path to your mosaic dataset.
  - "outputDir": "/data/sharedData/directories/arcgisoutput" - Set "outputDir" to be the location of the **arcgisoutput** folder.
  -  "onlineResource": "https://ps0009281.esri.com:6443/arcgis/service/GPM_2019/ImageServer/WCSServer" of "typeName": "WCSServer" - Set this to be your server URL/arcgis/service/servicename/ImageServer/WCSServer
  - "onlineResource": "https://ps0009281.esri.com:6443/arcgis/service/GPM_2019/ImageServer/WMSServer" of "typeName": "WMSServer" - Set this to be your server URL/arcgis/service/servicename/ImageServer/WMSServer
  
## Publish the image service through the ArcGIS Admin page
Here, the ArcGIS Server I am using is **https://ps0009281.esri.com**. Please modify your URLs accordingly.

1. Log into the ArcGIS Server Admin page: **https://ps0009281.esri.com:6443/arcgis/admin**.
2. Click on **services**. It will take you to **/arcgis/admin/services**.
3. Click on **createService** at the bottom of the page. It will take you to **arcgis/admin/services/createService**.
4. In the text box, past your image service JSON that you cnofigured above.
5. Change the format from **HTML** to **JSON**.
6. Click the **Create** button.

The service will publish. This could take a minute. My resulting service URL was **https://ps0009281.esri.com:6443/arcgis/rest/services/GPM_2019_Demo/ImageServer**.

