import json
import requests
import argparse
from config import config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='client.py')
    parser.add_argument('method', type=str)
    parser.add_argument('-message', type=str)
    args = parser.parse_args()
    
    if args.method == "post":
        response = requests.post(config["facade"], json={"message": args.message})
        print(response.json())
    else:
        response = requests.get(config["facade"])
        try:
            data = response.json()
            print(data)
        except requests.exceptions.JSONDecodeError:
            print("Error: Received non-JSON response")
            print(response.text)
