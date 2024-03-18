import requests
import json

url = "http://localhost:5000/facade-service"

message = {"msg": "Hi!"}

response = requests.post(url, json=message)

if response.status_code == 200:
    print("Request successful.")
    print("Response ID:", response.text)
else:
    print("Request failed.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
