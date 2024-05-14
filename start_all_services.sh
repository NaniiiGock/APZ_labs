#!/bin/bash

# Function to check if Consul is running
is_consul_running() {
    pgrep consul > /dev/null 2>&1
    return $?
}

# Function to wait until Consul is fully running
wait_for_consul() {
    while ! curl -s http://127.0.0.1:8500/v1/status/leader > /dev/null; do
        echo "Waiting for Consul to start..."
        sleep 2
    done
}

# Start Consul if it's not already running
if ! is_consul_running; then
    echo "Starting Consul agent..."
    consul agent -dev &
    CONSUL_PID=$!
    echo "Consul started with PID $CONSUL_PID"
else
    echo "Consul is already running"
fi

# Wait for Consul to be fully up and running
wait_for_consul
echo "Consul is running"

# Function to start a service
start_service() {
    local service=$1
    local host=$2
    local port=$3
    echo "Starting $service service on $host:$port"
    python "$service"_service.py "$host" "$port" &
    echo "$service service started"
}

# Start all services
start_service "facade" "127.0.0.1" "8081"
start_service "logging" "127.0.0.1" "8083"
start_service "logging" "127.0.0.1" "8085"
start_service "message" "127.0.0.1" "8086"

echo "All services started"
