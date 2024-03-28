import requests

query_par = {"user_id": "Lebron", "follower_id": "Ronaldo"}
response = requests.post("http://127.0.0.1:8000/follow", params=query_par)

print(response.text)