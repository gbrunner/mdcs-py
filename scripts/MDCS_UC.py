#------------------------------------------------------------------------------
# Copyright 2013 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#------------------------------------------------------------------------------
# Name: MDCS_UC.py
# Description: A class to implement all user functions or to extend the built in MDCS functions/commands chain.
# Version: 20171217
# Requirements: ArcGIS 10.1 SP1
# Author: Esri Imagery Workflows team
#------------------------------------------------------------------------------
#!/usr/bin/env python
import os
import sys
import arcpy
import datetime

class UserCode:

    def __init__(self):
        pass    # initialize variables that need to be shared between multiple user commands.

    def sample00(self, data):
        base = data['base']         # using Base class for its XML specific common functions. (getXMLXPathValue, getXMLNodeValue, getXMLNode)
        xmlDOM = data['mdcs']       # access to MDCS config file
        command_used = base.getXMLNodeValue(xmlDOM, 'Command')
        workspace = data['workspace']
        md = data['mosaicdataset']
        log = data['log']
        log.Message('%s\\%s' % (workspace, md), 0)
        return True

    def sample01(self, data):
        log = data['log']           # How to use logging within the user function.
        log.Message('hello world', 0)
        return True

    def customCV(self, data):
        workspace = data['workspace']
        md = data['mosaicdataset']
        ds = os.path.join(workspace, md)
        ds_cursor = arcpy.UpdateCursor(ds)
        if (ds_cursor is not None):
            print ('Calculating values..')
            row = ds_cursor.next()
            while(row is not None):
                row.setValue('MinPS', 0)
                row.setValue('MaxPS', 300)
                WRS_Path = row.getValue('WRS_Path')
                WRS_Row = row.getValue('WRS_Row')
                if (WRS_Path is not None and
                        WRS_Row is not None):
                    PR = (WRS_Path * 1000) + WRS_Row
                    row.setValue('PR', PR)
                AcquisitionData = row.getValue('AcquisitionDate')
                if (AcquisitionData is not None):
                    AcquisitionData = str(AcquisitionData).replace('-', '/')
                    day = int(AcquisitionData.split()[0].split('/')[1])
                    row.setValue('Month', day)
                grp_name = row.getValue('GroupName')
                if (grp_name is not None):
                    CMAX_INDEX = 16
                    if (len(grp_name) >= CMAX_INDEX):
                        row.setValue('DayOfYear', int(grp_name[13:CMAX_INDEX]))
                        row.setValue('Name', grp_name.split('_')[0] + '_' + row.getValue('Tag'))
                ds_cursor.updateRow(row)
                row = ds_cursor.next()
            del ds_cursor
        return True

    def addfields(self,data,inputfc,fldlst):
        try:
            for fld in fldlst:
                [[fldKey,fldValue]] = fld.items()
                fldName = fldKey
                fldType = fldValue[0]
                fldPrec = fldValue[1]
                fldScale = fldValue[2]
                fldLen = fldValue[3]
                try:
                    fldalias = fldValue[4]
                except:
                    fldalias = fldName
                arcpy.AddField_management(inputfc,fldName,fldType,fldPrec,fldScale,fldLen,field_alias=fldalias)
            return True
        except Exception as exp:
            print(str(exp))
            return False

    def buildSRCTable(self,data):
        base = data['base']         # using Base class for its XML specific common functions. (getXMLXPathValue, getXMLNodeValue, getXMLNode)
        xmlDOM = data['mdcs']       # access to MDCS config file
        inputmrf = base.getXMLNodeValue(xmlDOM, 'inputmrf')
        outFC = base.getXMLNodeValue(xmlDOM, 'outputsrcFC')
        startrange = base.getXMLNodeValue(xmlDOM, 'startdate')
        endrange = base.getXMLNodeValue(xmlDOM, 'enddate')
        startslice = int(base.getXMLNodeValue(xmlDOM, 'startslice'))
        endslice = int(base.getXMLNodeValue(xmlDOM, 'endslice'))
        interval = float(base.getXMLNodeValue(xmlDOM, 'interval'))
        intervalunits = base.getXMLNodeValue(xmlDOM, 'intervalunits') #months,weeks,days,hours,minutes,seconds
        bucketname = base.getXMLNodeValue(xmlDOM,'bucket')
        bucketdir = base.getXMLNodeValue(xmlDOM,'infolder')
        xmlDOM.getElementsByTagName("filter")[0].firstChild.data = "SyncDateTime > timestamp'{}'".format(datetime.datetime.now().replace(microsecond=0))  #Set a filter while doing add rasters
##        log.Message(xmlDOM.getElementsByTagName("filter")[0].firstChild.data,0)
        log = data['log']
        if intervalunits == 'months':
            timediff = datetime.timedelta(months=interval)
            incrStartTimeBy = datetime.timedelta(months=interval*startslice)
        elif intervalunits == 'weeks':
            timediff = datetime.timedelta(weeks=interval)
            incrStartTimeBy = datetime.timedelta(weeks=interval*startslice)
        elif intervalunits == 'days':
            timediff = datetime.timedelta(days=interval)
            incrStartTimeBy = datetime.timedelta(days=interval*startslice)
        elif intervalunits == 'hours':
            timediff = datetime.timedelta(hours=interval)
            incrStartTimeBy = datetime.timedelta(hours=interval*startslice)
        elif intervalunits == 'minutes':
            timediff = datetime.timedelta(minutes=interval)
            incrStartTimeBy = datetime.timedelta(minutes=interval*startslice)
        else:
            timediff = datetime.timedelta(seconds=interval)
            incrStartTimeBy = datetime.timedelta(seconds=interval*startslice)
        oMRF = open(inputmrf,"r")
        mrfLines = oMRF.readlines()
        oMRF.close()
        for line in mrfLines:
            line = line.strip()

            if line.startswith('<BoundingBox'):
                minx = float(line.split(" ")[1].split("=")[1].replace('"',''))
                miny = float(line.split(" ")[2].split("=")[1].replace('"',''))
                maxx = float(line.split(" ")[3].split("=")[1].replace('"',''))
                maxy = float(line.split(" ")[5].replace('"',''))

        sr = arcpy.SpatialReference(4326)
        if arcpy.Exists(outFC) == False:
            wrkSpace = os.path.dirname(outFC)
            if arcpy.Exists(wrkSpace) == False:         #build Geodatabase
                wrkSPath = os.path.dirname(wrkSpace)
                wrkSName = os.path.basename(wrkSpace)
                arcpy.CreateFileGDB_management(wrkSPath,wrkSName)
            featClassName = os.path.basename(outFC)
            geometryType = "POLYGON"
            template = "#"
            hasM = "DISABLED"
            hasZ = "DISABLED"
            arcpy.CreateFeatureclass_management(wrkSpace, featClassName, geometryType, template, hasM, hasZ, sr)
            fileFieldDef = []
            inputFLDLst = ['Name','Tag','Variable','Dimensions','Raster','StdTime','SyncDateTime']
            fileFieldDef.append({inputFLDLst[0]:['Text','#','#',100]}) #Name
            fileFieldDef.append({inputFLDLst[1]:['Text','#','#',50]})  #Tag
            fileFieldDef.append({inputFLDLst[2]:['Text','#','#',50]})  #Variable
            fileFieldDef.append({inputFLDLst[3]:['Text','#','#',50]}) #Dimensions
            fileFieldDef.append({inputFLDLst[4]:['Text','#','#',5000]}) #Raster
            fileFieldDef.append({inputFLDLst[5]:['Date','#','#','#','StandardTime']})  #StdTime
            fileFieldDef.append({inputFLDLst[6]:['Date','#','#','#']})  #SyncDateTime is used to identify the newly added data.
            self.addfields(data,outFC,fileFieldDef)

        else:
            log.Message("New records will be appended to the existing feature class",1)

        ic = arcpy.da.InsertCursor(outFC,['Name','Tag','Variable','Dimensions','Raster','SHAPE@','StdTime','SyncDateTime'])
        variable = 'precipitationCal'
        dimension = 'StdTime'
        tag = 'precipitationCal'
        polysr = arcpy.SpatialReference(3857)
        srstring = arcpy.SpatialReference(4326).exportToString()
        i = 0
        s_dt = datetime.datetime.strptime(startrange,"%Y/%m/%dT%H:%M:%S.%f") #start datetime of the mrf file.
        e_dt = datetime.datetime.strptime(endrange,"%Y/%m/%dT%H:%M:%S.%f")
        newdt = s_dt + incrStartTimeBy  #modify the start datetime based on the start slice count.
        s_slice = startslice
        while (newdt <= e_dt) and s_slice <= endslice:
            val = []
            mrfname = os.path.basename(inputmrf).split(".")[0]
            name = mrfname + "_{0}".format(str(s_slice))
            try:
                if bucketname != "#":
                    if bucketdir != "#":
                        rp ='<MRF_META>\n' \
                        '  <CachedSource>\n' \
                        '    <Source>/vsicurl/http://{0}.s3.amazonaws.com/{1}/{2}.mrf:MRF:Z{3}</Source>\n' \
                        '  </CachedSource>\n' \
                        '  <Raster>\n' \
                        '    <Size x="3600" y="1800" c="1" />\n' \
                        '    <PageSize x="450" y="450" c="1" />\n' \
                        '    <Compression>LERC</Compression>\n' \
                        '    <DataType>Float32</DataType>\n' \
                        '    <DataValues NoData="-9999" />\n' \
                        '    <DataFile>/arcgis-dev-mosaic-share/mrfcache/gpm/{4}.mrf_cache</DataFile><IndexFile>/arcgis-dev-mosaic-share/mrfcache/gpm/{4}.mrf_cache</IndexFile></Raster>\n'  \
                        '  <GeoTags>\n' \
                        '    <BoundingBox minx="-179.99999695" miny="-89.99999695" maxx="179.99999695" maxy=" 89.99999695" />\n' \
                        '    <Projection>{5}</Projection>\n' \
                        '  </GeoTags>\n' \
                        '  <Options>LERC_PERC=0.0001 V2=ON</Options>\n' \
                        '  <Rsets model="uniform" scale="2" />\n' \
                        '</MRF_META>\n'.format(bucketname,bucketdir,mrfname,s_slice,name,srstring)
                    else:
                        log.Message("No bucket directory is specified. Quiting the program")
                        exit()
                else:
                    rp ='<MRF_META>\n' \
                    '  <CachedSource>\n' \
                    '    <Source>{0}:MRF:Z{1}</Source>\n' \
                    '  </CachedSource>\n' \
                    '  <Raster>\n' \
                    '    <Size x="3600" y="1800" c="1" />\n' \
                    '    <PageSize x="450" y="450" c="1" />\n' \
                    '    <Compression>LERC</Compression>\n' \
                    '    <DataType>Float32</DataType>\n' \
                    '    <DataValues NoData="-9999" />\n' \
                    '    <DataFile>/arcgis-dev-mosaic-share/mrfcache/gpm/{2}.mrf_cache</DataFile><IndexFile>/arcgis-dev-mosaic-share/mrfcache/gpm/{2}.mrf_cache</IndexFile></Raster>\n'  \
                    '  <GeoTags>\n' \
                    '    <BoundingBox minx="-179.99999695" miny="-89.99999695" maxx="179.99999695" maxy=" 89.99999695" />\n' \
                    '    <Projection>{3}</Projection>\n' \
                    '  </GeoTags>\n' \
                    '  <Options>LERC_PERC=0.0001 V2=ON</Options>\n' \
                    '  <Rsets model="uniform" scale="2" />\n' \
                    '</MRF_META>\n'.format(inputmrf,s_slice,name,srstring)
##                    rp="{0}:MRF:{1}".format(inputmrf,i)  This representation is not supported
                standTime = newdt
                coords = [[minx,miny],[maxx,miny],[maxx,maxy],[minx,maxy],[minx,miny]]
                pointarray = arcpy.Array()
                for point in coords:
                    point = arcpy.Point(point[0],point[1])
                    pointarray.add(point)
                poly = arcpy.Polygon(pointarray,sr)
    ##                poly = poly.projectAs(polysr)
                val.append(name)
                val.append(tag)
                val.append(variable)
                val.append(dimension)
                val.append(rp)
                val.append(poly)
                val.append(standTime)
                val.append(datetime.datetime.now())
                ic.insertRow(val)
                newdt = newdt + timediff
                i+=1
                s_slice+=1
            except Exception as exp:
                log.Message(str(exp),2)
        del ic
        return True
