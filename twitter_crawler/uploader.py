import requests

def upload(data,path):
    SERVER_URL = "http://172.26.134.122"
    try:
        response = requests.post(SERVER_URL+path, json=data,timeout=100000)
    except Exception as e:
        print(e)
    print(response.text)
    return response