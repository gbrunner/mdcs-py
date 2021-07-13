from arcgis.gis import GIS
from arcgis.mapping import WebMap
import json



gis = GIS("https://ps0010786.esri.com/portal/home/", "portaladmin", 'testThing11', verify_cert=False) 
#Set this to your portal and credentials, They should be able to set this to verify_cert=True
webmap_id = "9b625aaf5cfd43e8af6c496e8151ff1c" #Set this to your webmap ID


webmap_item = gis.content.get(webmap_id)
webmap_data = webmap_item.get_data()

print(webmap_data)



#webmap_data['widgets']['timeSlider']['properties']['startTime'] = 1556300800000
webmap_data['widgets']['timeSlider']['properties']['timeStopInterval']['interval'] = 60
webmap_data['widgets']['timeSlider']['properties']['timeStopInterval']['units'] = 'esriTimeUnitsMinutes'
webmap_data['widgets']['timeSlider']['properties']['currentTimeExtent'] = [1558560000000, 1558561800000] #update this everyday
webmap_item.update(data=json.dumps(webmap_data))

print("Done.")