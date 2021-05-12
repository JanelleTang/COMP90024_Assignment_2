import json
import ujson
import pandas as pd
from geopy.geocoders import Nominatim
from collections import defaultdict as dd

# ============================== use data from couch ============================== #
with open('/Users/janelletang/Documents/GitHub/CCC_backend/backend/locations/analytics/data/tweets.json','r') as f:
    file = json.load(f)['rows']
    data = [x['doc'] for x in file]

    data = pd.DataFrame.from_dict(data)


regions_dict = {}


def get_lga_data(filepath,geom_field,name_field,state,excluded):
    with open(filepath,"r") as f:
        lga = json.load(f)
        for feature in lga['features']:
            poly = feature[geom_field]
            lga_name = feature['properties'][name_field]
            if any(word in lga_name for word in excluded ):
                continue
            regions_dict[lga_name.lower()] = {"geometry":poly}

## MELBOURNE LGA DATA
get_lga_data("locations/analytics/data/VIC_LGA.geojson.json","geometry","SH_NAME","vic",["SHIRE","RURAL","ALPINE","GREATER","("])
## ADELAIDE LGA DATA
get_lga_data("locations/analytics/data/SA_LGA.geojson.json","geometry","lga","sa",["RURAL","UNINCORPORATED"])
## SYDNEY LGA DATA
get_lga_data("locations/analytics/data/NSW_LGA.geojson.json","geometry","nsw_lga_2","nsw",["SHIRE","RURAL","UNINCORPORATED","REGIONAL"])
## BRISBANE LGA DATA
get_lga_data("locations/analytics/data/QLD_LGA.geojson.json","geometry","qld_lga__2","qld",["SHIRE","RURAL","ISLAND","REGIONAL"])



# ============================== Converting location to coordinates ============================== #
geolocator = Nominatim(user_agent="tweets")

def locator(locale):
    location = geolocator.geocode(locale,addressdetails=True)
    address = location.raw['address'] # If we want more accuracy
    if address['country']!="Australia":
        print("Check this tweet location")
        return None,None
    if len(address) <3:
        return None,None,None
    return (location.latitude, location.longitude),address["municipality"].lower(),address["state"].lower()


results = dd(lambda: dd(int))
for i,row in data.iterrows():
    location = row["user location"]
    coordinates,lga,state = locator(location)
    if lga == None:
        continue
    n_sent = row["sentiment_value"]
    results[lga]["state"]=state
    results[lga]["geometry"] = regions_dict[lga]['geometry']
    results[lga]["total_sentiment"]+=float(n_sent)
    results[lga]["total_tweets"]+=1

with open('locations/analytics/data/regions_data.json', 'w') as fp:
    ujson.dump(results, fp)