import uvicorn
import argparse
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    uuid: str

app = FastAPI()

@app.get('/')
def home():
    print("Getting messages...")
    return "Not implemented"

@app.post("/")
def post_msg(msg: Message):
    return "Not implemented"

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog = 'message_service.py')
    parser.add_argument('host', type=str) 
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    
    print("Running message service...")
    uvicorn.run("message_service:app", 
                host=args.host, 
                port=args.port, 
                reload=False)