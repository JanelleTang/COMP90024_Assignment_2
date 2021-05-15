import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

lga_dict = {}

def get_lga_data(filepath,name_field):
    with open(filepath,"r") as f:
        lga = json.load(f)
        for feature in lga['features']:
            poly = feature["geometry"]
            try:
                address = geolocator.geocode(feature['properties'][name_field],addressdetails=True,timeout=1000).raw['address']
                lga_name = address["municipality"].lower()
            except:
                lga_name = feature['properties'][name_field]
                lga_dict[lga_name.lower()] = {"geometry":poly}
                return
            lga_dict[lga_name.lower()] = {"geometry":poly}

geolocator = Nominatim(user_agent="region_data")     

## VIC LGA DATA
get_lga_data("shapefiles/VIC_LGA.geojson.json","SH_NAME")
## SA LGA DATA
get_lga_data("shapefiles/SA_LGA.geojson.json","lga")
## NSW LGA DATA
get_lga_data("shapefiles/NSW_LGA.geojson.json","nsw_lga_2")
## QLD LGA DATA
get_lga_data("shapefiles/QLD_LGA.geojson.json","qld_lga__2")
## TAS LGA DATA
get_lga_data("shapefiles/TAS_LGA.geojson.json","tas_lga__2")
## WA LGA DATA
get_lga_data("shapefiles/WA_LGA.geojson.json","wa_lga_s_2")

with open('shapefiles/combined_lga_data.json','w') as f:
    json.dump(lga_dict,f)



