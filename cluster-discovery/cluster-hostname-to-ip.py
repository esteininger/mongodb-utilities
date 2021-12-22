import requests
from requests.auth import HTTPDigestAuth
import json
import socket

url = "https://cloud.mongodb.com/api/atlas/v1.0"
HEADERS = {'Content-Type':'application/json','Accept':'application/json'}


pub = ""
priv = ""

list_of_clusters = requests.get(url=url+'/groups', headers=HEADERS, auth=HTTPDigestAuth(pub, priv)).json()
# print(list_of_clusters)

for cluster in list_of_clusters['results']:
    group = cluster['id']
    name = cluster['name']
    append = f'/groups/{group}/clusters/HACKATHON'
    r = requests.get(url=url+append, headers=HEADERS, auth=HTTPDigestAuth(pub, priv)).json()
    try:
        array_of_hostnames = r['mongoURI'].split(',')
        arr = []
        for hostname in array_of_hostnames:
            a = hostname.replace('mongodb://','').replace(':27017', '')
            ip = socket.gethostbyname(a)
            arr.append(ip)
        print(name, arr, r['mongoURI'])
    except:
        pass
