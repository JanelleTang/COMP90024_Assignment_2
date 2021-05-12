## file to create aurin.json from csv files

import pandas as pd
import re
import json
import couchdb
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="tweets")

## local host credentials here - need to change to local instance
couch = couchdb.Server('http://admin:password@localhost:5984/')

db = couch['aurin_data']

dataDict = {}
for file in [{'file_name' : 'OCCUPANCY_1991.csv','index' : ' lga_name_1991'},
             {'file_name' : 'INDUSTRY_EMPLOYMENT_2016.csv','index' : ' lga_name16'},
             #{'file_name' : 'LABOR_FORCE_STATUS_EDUCATION_2016.csv','index' : ' sa2_name16'},
             {'file_name' : 'LGA_ENERGY_ENVIRON_2010_2014.csv','index' : ' lga_name_2014'},
             {'file_name' : 'INCOME_AND_AGE_2016.csv','index' : ' lga_name_2016'},
             {'file_name' : 'LGA_PROFILES_2015.csv','index' : ' lga_name'}
    ]:
    print(file)
    dataFile = pd.read_csv(file['file_name'],
                           index_col=file['index'])

    dataFile = dataFile.fillna(0)

    for key, values in dataFile.iterrows():
        try:
            location = geolocator.geocode(key + ", Australia",addressdetails=True)
        except:
            continue
        if location is None:
            continue
        address = location.raw["address"]
        if 'municipality' not in address:
            continue
        lga = address['municipality'].lower()
        print(lga)
        city = address.get('city','none').lower()
        state = address.get('state','none').lower()
        if lga not in dataDict:
            dataDict[lga] = {'lga' : lga, 'city' : city, 'state' : state}
        if file['file_name'] == 'LGA_ENERGY_ENVIRON_2010_2014.csv':
            dataDict[lga]['solarPanels'] = dataDict[lga].get('solarPanels',0) + values[' solar_panel_system']
            dataDict[lga]['solarWaterHeaters'] = dataDict[lga].get('solarWaterHeaters',0) + values[' solar_water_heater']
        if file['file_name'] == 'LGA_PROFILES_2015.csv':
            dataDict[lga]['homeless_perc'] =  values[' homeless_ppl_est_per_1000_pop']
            dataDict[lga]['aboriginal_origin'] = values[' ppl_of_aboriginal_and_torres_strait_islander_orgn_perc']
            dataDict[lga]['pleasant_community'] = values[' ppl_who_rated_their_cmty_as_a_pleasant_env_perc']
            dataDict[lga]['gaming_losses'] = values[' gaming_machine_losses_per_adult_pop_aud']
            dataDict[lga]['students'] = values[' full_time_equivalent_students_perc']
            dataDict[lga]['multiculturalism_opinion'] = values[' ppl_who_believe_multiculturalism_makes_life_better_perc']
        if file['file_name'] == 'OCCUPANCY_1991.csv':
            for colName,value in zip(values.index,values):
                if re.match(r"^ rent",colName):
                    dataDict[lga]['renters'] = dataDict[lga].get('renters',0) + value
                elif re.match(r"^ owned",colName):
                    dataDict[lga]['owned'] = dataDict[lga].get('owned',0) + value
                elif re.match(r"^ being",colName):
                    dataDict[lga]['being_purcahsed'] = dataDict[lga].get('being_purcahsed',0) + value
        if file['file_name'] == 'INDUSTRY_EMPLOYMENT_2016.csv':
            for colName,value in zip(values.index,values):
                if re.search(r"tot\_p$",colName):
                    dataDict[lga]['industry_total_pop'] = dataDict[lga].get('industry_total_pop',0) + value
                if colName == ' egwws_gassup_p':
                    dataDict[lga]['ind_gas_supply'] = dataDict[lga].get('ind_gas_supply',0) + value
                if colName == ' egwws_total_p':
                    dataDict[lga]['ind_energy'] = dataDict[lga].get('ind_energy',0) + value
                if colName == ' min_coal_min_p':
                    dataDict[lga]['ind_coal'] = dataDict[lga].get('ind_coal',0) + value
                if colName == ' min_tot_p':
                    dataDict[lga]['ind_mining'] = dataDict[lga].get('ind_mining',0) + value
        if file['file_name'] == 'INCOME_AND_AGE_2016.csv':
            for colName,value in zip(values.index,values):
                if colName == ' p_tot_tot':
                    dataDict[lga]['age_income_tot'] = dataDict[lga].get('age_income_tot',0) + value
                if (re.search(r"tot\_15\_19",colName) or re.search(r"tot\_20\_24",colName) or
                    re.search(r"tot\_25\_34",colName)):
                    dataDict[lga]['age_under_35'] = dataDict[lga].get('age_under_35',0) + value
                if (re.search(r"3000\_more\_tot",colName)):
                    dataDict[lga]['weekly_income_over_3000'] = dataDict[lga].get('weekly_income_over_3000',0) + value
                if (re.search(r"1000\_1249\_tot",colName)):
                    dataDict[lga]['weekly_income_under_1250'] = dataDict[lga].get('weekly_income_under_1250',0) + value

with open("aurin.json",'w') as file:
    json.dump(dataDict,file)
'''
try:
    db.delete(db['lga_data'])
except:
    pass
db['lga_data'] = dataDict
'''
        

