import consul
import socket

def register_service(service_name, service_id, service_port):
    c = consul.Consul()
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    
    c.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=host_ip,
        port=service_port,
        tags=["primary"]
    )

def deregister_service(service_id):
    c = consul.Consul()
    c.agent.service.deregister(service_id)
