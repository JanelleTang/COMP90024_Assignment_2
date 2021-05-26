# ============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== 
import json

lga_dict = {}

def get_lga_data(filepath,name_field):
    with open(filepath,"r") as f:
        lga = json.load(f)
        for feature in lga['features']:
            poly = feature["geometry"]
            lga_name = feature['properties'][name_field]
            lga_dict[lga_name.lower()] = {"geometry":poly}

            
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

