import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import argparse
import hazelcast

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()
client = hazelcast.HazelcastClient()
hash_map = client.get_map("my_map").blocking()

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
