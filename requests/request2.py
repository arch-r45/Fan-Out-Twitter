import requests

query_par = {"username": "dumber", "password": "barktree"}
response = requests.post("http://127.0.0.1:8000/signin", params=query_par)

print(response.text)