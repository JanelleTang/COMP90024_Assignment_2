import requests

def upload(data,path):
    SERVER_URL = "http://127.0.0.1:8000"
    response = requests.post(SERVER_URL+path, json=data,timeout=100)
    with open("response_text.html","w") as f:
        f.write(str(response.text))
    return response