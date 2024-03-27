import requests

query_par = {"user_id": "Ronaldo", "tweet": "I have playing in Abu Dhabi"}
response = requests.post("http://127.0.0.1:8000/update", params=query_par)

print(response.text)