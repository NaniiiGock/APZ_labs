import json
import requests
import argparse
from config import config
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'client.py')
    parser.add_argument('method', type=str)
    parser.add_argument('-message', type=str)
    args = parser.parse_args()
    
    if args.method == "post":
        requests.post(config["facade"], json.dumps({"message": args.message}))
    else:
        print(requests.get(config["facade"]).json().split(":")[0])