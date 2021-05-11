import http.client
import ujson

def upload(data, path):
    SERVER_URL = "http://localhost:8000"
    response_body = {
        "data" : data
    }
    response_body = ujson.encode(response_body)
    connection = http.client.HTTPSConnection(SERVER_URL)
    connection.request("POST", path, response_body)
    response = connection.getresponse()
    response = ujson.load(response)
    return response