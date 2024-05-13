# import uvicorn
# import argparse
# from fastapi import FastAPI
# from pydantic import BaseModel
# import hazelcast
# import asyncio

# class Message(BaseModel):
#     message: str
#     uuid: str

# app = FastAPI()
# client = hazelcast.HazelcastClient()
# queue = client.get_queue("queue").blocking()
# message_list = []

# @app.get('/')
# async def home():
#     global message_list
#     messages = message_list[:]
#     message_list.clear()
#     print("Getting messages...\n", messages)
#     return {"messages": messages}

# @app.post("/")
# def post_msg(msg: Message):
#     print(f"Message service received post request: {msg}")
#     return "to be implemented"

# async def put_to_queue():
#     global message_list
#     while True:
#         item = queue.take()
#         if item:
#             message_list.append(item)
#             print(f"Message service received from queue: {item}")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(prog='message_service.py')
#     parser.add_argument('host', type=str)
#     parser.add_argument('port', type=int)
#     args = parser.parse_args()
    
#     loop = asyncio.get_event_loop()
#     loop.create_task(put_to_queue())
#     uvicorn.run(app, host=args.host, port=args.port)


from quart import Quart, jsonify, request
import hazelcast
import argparse
import asyncio
from asyncio import Queue

messages = Queue()  
app = Quart(__name__)

async def poll_queue(queue, messages):
    while True:
        future = await asyncio.to_thread(queue.take)
        if future is not None:
            await messages.put(future)
            print(f"Message accepted: {future}")

@app.route('/messages')
async def return_messages():
    messages_list = []
    while not messages.empty():
        messages_list.append(await messages.get())
    print(f"Returning Messages: {messages_list}")
    return jsonify(messages=messages_list)

async def main(host, port):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue").blocking()

    asyncio.create_task(poll_queue(queue, messages))

    await app.run_task(host=host, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='message_service.py')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()

    asyncio.run(main(args.host, args.port))

