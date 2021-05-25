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

import requests

def upload(data,path):
    SERVER_URL = "http://172.26.134.122"
    try:
        response = requests.post(SERVER_URL+path, json=data,timeout=100000)
    except Exception as e:
        print(e)
    print(response.text)
    return response
