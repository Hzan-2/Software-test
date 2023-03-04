import json
import requests

def post_api(url,data,headers=None):
    return json.loads(requests.post(url,data=json.dumps(data),headers=headers).text)

def get_api(url,headers=None):
    return json.loads(requests.get(url, headers=headers).text)