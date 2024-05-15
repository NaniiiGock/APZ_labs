#!/bin/bash

clear_port() {
    local port=$1
    if lsof -i:$port > /dev/null; then
        echo "Clearing port $port..."
        lsof -ti:$port | xargs kill -9
    fi
}


ports_to_clear=(8081 8082 8083 8084 8085)


for port in "${ports_to_clear[@]}"; do
    clear_port $port
done

echo "Starting facade service on port 8081..."
python facade_service.py 127.0.0.1 8081 &


echo "Starting message service on port 8082..."
python message_service.py 127.0.0.1 8082 &


for port in 8083 8084 8085; do
    echo "Starting logging service on port $port..."
    python logging_service.py 127.0.0.1 $port &
done


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
