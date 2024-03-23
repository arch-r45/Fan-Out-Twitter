import requests

query_par = {"user_id": "dumber", "tweet": "Welcome to Twitter!"}
response = requests.post("http://127.0.0.1:8000/update", params=query_par)

print(response.text)