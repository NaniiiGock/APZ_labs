import uuid
import json
import random
import uvicorn
import argparse
import requests
import hazelcast
import consul
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
consul_client = consul.Consul()
client = None
queue = None

@app.on_event("startup")
async def startup_event():
    global client, queue
    index, data = consul_client.kv.get('message_queue/config')
    if data is None:
        raise ValueError("Message queue config not found in Consul")
    message_queue_config = json.loads(data['Value'])
    client = hazelcast.HazelcastClient()  # Use message_queue_config if needed
    queue = client.get_queue(message_queue_config['queue_name']).blocking()
    register_service()

def register_service():
    consul_client.agent.service.register(
        "facade-service",
        service_id="facade-service",
        address="127.0.0.1",
        port=8081,
        tags=["facade"]
    )

@app.get('/')
def home():
    print("Facade getting messages...")
    try:
        services = consul_client.health.service("logging-service")[1]
        logging_service = random.choice(services)["Service"]
        logging_url = f"http://{logging_service['Address']}:{logging_service['Port']}"
        logging_response = requests.get(logging_url)
        logging_response.raise_for_status()
        print(f"Logging service URL used: {logging_url}")
        print(f"Logging service response: {logging_response.text}")

        services = consul_client.health.service("message-service")[1]
        message_service = random.choice(services)["Service"]
        message_url = f"http://{message_service['Address']}:{message_service['Port']}/messages"
        message_response = requests.get(message_url)
        message_response.raise_for_status()
        print(f"Message service URL used: {message_url}")
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
    data = {"message": data.get("message"), "uuid": str(uuid.uuid4())}
    queue.put(data)
    print(f"Facade service put message in queue: {data}")
    services = consul_client.health.service("logging-service")[1]
    logging_service = random.choice(services)["Service"]
    logging_url = f"http://{logging_service['Address']}:{logging_service['Port']}"
    print(f"Posting {data['uuid']}: {data['message']} to logging service URL: {logging_url}")
    requests.post(logging_url, json=data)
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
