from sentiment_analyser import *
from datetime import datetime
import requests
import sys
from time import sleep
from uploader import upload

## Processing and aggregating tweets ##
def tweet_processor(tweets):
    regions_lst = []
    for data in tweets:
        for k,tweet in data.items():
            text = tweet['text']
            date_string = tweet['date_created']
            date_formatted,time_formatted = convert_date_format(date_string)
            if tweet['geo']: 
                location = tweet['geo']
                geo = True
            else:
                location = tweet['location']
                geo = False
            tweet_obj = CleanTweet(text,location,tweet['hashtags'],geo)
            region_data = tweet_obj.get_dict()
            if region_data != None:
                region_data['date'] = date_formatted
                region_data['time'] = time_formatted
                regions_lst.append(region_data)
    return {"data":regions_lst}
def dict_uploader(data,path):
    response = upload(data, path)
    print(response)
def convert_date_format(date_string):
    try:
        time_obj = datetime.strptime(date_string,'%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            time_obj = datetime.strptime(date_string,'%a %b %d %H:%M:%S +0000 %Y')
        except:
            return "unknown","unknown"
    formatted_time = datetime.strftime(time_obj, '%H')
    formatted_date = datetime.strftime(time_obj.date(), '%Y-%m-%d')
    return formatted_date,formatted_time
if __name__ == '__main__':
    path = 'http://172.26.134.122'
    try:
        while True:
            try:
                print("Restarting regions uploader...")
                tweets = requests.get(URL +'/api/tweet/raw/100').json()['obj']
                regions_data = tweet_processor(tweets)
                dict_uploader(regions_data,"/api/location/create")
                print("Creating Model Instances...")
                requests.get("http://172.26.134.122:8000/location/update/city")
                requests.get("http://172.26.133.17:8000/location/update/city")
                requests.get("http://172.26.133.243:8000/location/update/city")
                sleep(10)
                requests.get("http://172.26.134.122:8000/location/update/lga")
                requests.get("http://172.26.133.17:8000/location/update/lga")
                requests.get("http://172.26.133.243:8000/location/update/lga")
                sleep(1800)
            except requests.exceptions.ConnectionError:
                print("Connection Error. Please Wait...")
                sleep(100)
                continue
    except:
        e = sys.exc_info()[0]
        print(e)