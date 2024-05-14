# consul_utils.py
import consul
import socket
import json
import random

def register_service(consul_client, service_name, service_port):
    service_id = f"{service_name}-{service_port}"
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    consul_client.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=ip_address,
        port=service_port,
        tags=[service_name]
    )
    print(f"Registered {service_name} with Consul at {ip_address}:{service_port}")

def get_service(consul_client, service_name):
    services = consul_client.health.service(service_name, passing=True)[1]
    service = random.choice(services)['Service']
    return service['Address'], service['Port']

def get_config(consul_client, key):
    _, data = consul_client.kv.get(key)
    if data:
        return json.loads(data['Value'])
    return None
