import uuid
import json
import random
import uvicorn
import argparse
import requests
from config import config
from fastapi import FastAPI, Request, HTTPException
import hazelcast

app = FastAPI()
client = hazelcast.HazelcastClient()
queue = client.get_queue("queue").blocking()

@app.get('/')
def home():
    print("Facade getting messages...")
    try:
        chosen_logging_url = random.choice(config['logging'])
        logging_response = requests.get(chosen_logging_url)
        logging_response.raise_for_status()
        print(f"Logging service URL used: {chosen_logging_url}")
        print(f"Logging service response: {logging_response.text}")

        chosen_message_url = random.choice(config['message'])
        message_response = requests.get(f"{chosen_message_url}/messages")
        message_response.raise_for_status()
        print(f"Message service URL used: {chosen_message_url}")
        print(f"Message service response: {message_response.json()}")

        logging_data = logging_response.json()
        message_data = message_response.json()
        
        if not isinstance(logging_data, dict) or not isinstance(message_data, dict):
            raise HTTPException(status_code=500, detail="Invalid JSON response format")

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "logging": logging_data.get("logs", ""),
        "message": message_data.get("messages", "")
    }

@app.post("/")
async def post_msg(msg: Request):
    data = await msg.json()
    data = {"message": data.get("message"), 
            "uuid": str(uuid.uuid4())}
    queue.put(data)
    print(f"Facade service put message in queue: {data}")
    chosen_logging_url = random.choice(config['logging'])
    print(f"Posting {data['uuid']}: {data['message']} to logging service URL: {chosen_logging_url}")
    requests.post(chosen_logging_url, json=data)
    return data['uuid']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='facade_service.py')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    print("Running facade...")
    uvicorn.run("facade_service:app", 
                host=args.host, 
                port=args.port, 
                reload=False)
