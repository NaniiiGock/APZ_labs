from quart import Quart, jsonify, request
import hazelcast
import argparse
import asyncio
import consul
import json
from asyncio import Queue

messages = Queue()
app = Quart(__name__)
consul_client = consul.Consul()

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

def register_service():
    consul_client.agent.service.register(
        "message-service",
        service_id="message-service",
        address="127.0.0.1",
        port=8082,
        tags=["message"]
    )

@app.before_serving
async def startup():
    global client, queue
    register_service()
    index, data = consul_client.kv.get('message_queue/config')
    if data is None:
        raise ValueError("Message queue config not found in Consul")
    message_queue_config = json.loads(data['Value'])
    client = hazelcast.HazelcastClient()  # Use message_queue_config if needed
    queue = client.get_queue(message_queue_config['queue_name']).blocking()
    asyncio.create_task(poll_queue(queue, messages))

async def main(host, port):
    await app.run_task(host=host, port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='message_service.py')
    parser.add_argument('host', type=str)
    parser.add_argument('port', type=int)
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port))
