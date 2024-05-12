import uuid
import json
import random
import uvicorn
import argparse
import requests
from config import config
from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/')
def home():
    print("Facade getting messages...")
    logging_response = requests.get(random.choice(config['logging']))
    messaging_response = requests.get(config['message'])
    return f"{logging_response.text}: {messaging_response.text}"

@app.post("/")
async def post_msg(msg: Request):
    
    data = await msg.json()
    data = {"message": data.get("message"), 
            "uuid": str(uuid.uuid4())}
    
    print(f"Posting {data['uuid']}: {data['message']}")
    requests.post(random.choice(config['logging']), json.dumps(data))
    requests.post(config['message'], json.dumps(data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'facade_service.py')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    print("Running facade...")
    uvicorn.run("facade_service:app", 
                host=args.host, 
                port=args.port, 
                reload=False)