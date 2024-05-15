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
        print(f"Post response: {response.text}")
    else:
        response = requests.get(config["facade"])
        print(f"Get response: {response.json().split(':')[0]}")
