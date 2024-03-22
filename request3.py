import requests

query_par = {"user_id": "dumber", "follower_id": "Justinbieber"}
response = requests.post("http://127.0.0.1:8000/follow", params=query_par)

print(response.text)