#!/bin/bash

# Function to clear a port
clear_port() {
    local port=$1
    if lsof -i:$port > /dev/null; then
        echo "Clearing port $port..."
        lsof -ti:$port | xargs kill -9
    fi
}

# Ports to clear
ports_to_clear=(8081 8082 8083 8084 8085)

# Clear the specified ports
for port in "${ports_to_clear[@]}"; do
    clear_port $port
done

# Run the facade service
echo "Starting facade service on port 8081..."
python facade_service.py 127.0.0.1 8081 &

# Run the message service
echo "Starting message service on port 8082..."
python message_service.py 127.0.0.1 8082 &

# Run logging services on the specified ports
for port in 8083 8084 8085; do
    echo "Starting logging service on port $port..."
    python logging_service.py 127.0.0.1 $port &
done

# Give the services a moment to start up
sleep 5

# Post messages 1 to 10
# for i in {1..10}; do
#     echo "Posting message $i..."
#     python client.py post -message "Message $i"
# done

# Get messages
# echo "Getting messages..."
# python client.py get

# echo "All services and client operations completed."
