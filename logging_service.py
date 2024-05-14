import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import argparse
import hazelcast
import consul
import json

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()
consul_client = consul.Consul()
client = None
hash_map = None

@app.on_event("startup")
async def startup_event():
    global client, hash_map
    index, data = consul_client.kv.get('hazelcast/config')
    if data is None:
        raise ValueError("Hazelcast config not found in Consul")
    hazelcast_config = json.loads(data['Value'])
    client = hazelcast.HazelcastClient()  # Use hazelcast_config if needed
    hash_map = client.get_map("my_map").blocking()
    register_service()

def register_service():
    consul_client.agent.service.register(
        "logging-service",
        service_id="logging-service",
        address="127.0.0.1",
        port=8083,
        tags=["logging"]
    )

@app.get('/')
def get_logs():
    print("Getting logs...")
    logs = "; ".join(list(hash_map.values()))
    return {"logs": logs}

@app.post("/")
def post_msg(msg: Message):
    print(f"Logging got {msg.uuid}: {msg.message}")
    hash_map.put(msg.uuid, msg.message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='logging_service.py')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    print("Running logging...")
    uvicorn.run("logging_service:app",
                host=args.host,
                port=args.port,
                reload=False)
