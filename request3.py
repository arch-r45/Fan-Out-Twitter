import requests

query_par = {"user_id": "Wayne", "follower_id": "Lebron"}
response = requests.post("http://127.0.0.1:8000/follow", params=query_par)

print(response.text)