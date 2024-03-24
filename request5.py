import requests

query_par = {"user_id": "Wayne"}
response = requests.get("http://127.0.0.1:8000/timeline", params=query_par)

print(response.text)