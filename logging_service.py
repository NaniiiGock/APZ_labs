
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import argparse
import hazelcast

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()

@app.get('/')
def get_logs():
    print("getting logs...")
    hash_map = hazelcast.HazelcastClient().get_map("my_map")
    return "; ".join(list(hash_map.values().result()))

@app.post("/")
def post_msg(msg: Message):
    hash_map = hazelcast.HazelcastClient().get_map("my_map")
    print(f"Logging got{msg.uuid}: {msg.message}")
    hash_map.put(msg.uuid, msg.message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'logging_service.py')
    parser.add_argument('host', type=str) 
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    print("Running logging...")
    uvicorn.run("logging_service:app", 
                host=args.host, 
                port=args.port, 
                reload=False)

