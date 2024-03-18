
# Flask Application Setup and Testing Report

## Overview

Setting up a Flask application with multiple services, including a facade service that acts as an intermediary between a client and other services. 

Description covers the initial setup, testing methods using `curl` from the terminal

## Application Structure

The Flask application is structured into three main components:

1. **Facade Service (`facade_service.py`):** Serves as the entry point for clients, aggregating data from the logging and message services.
2. **Logging Service (`logging_service.py`):** Logs messages received from the facade service.
3. **Messages Service (`messages_service.py`):** Provides a static message response.

## Setting Up

### Requirements

- Python 3
- Flask
- requests
- Flask-CORS

```sh
pip install Flask requests Flask-CORS
```

### Running the Services
Each service runs on its own port. Use separate terminal windows or sessions to start each service


### Testing the Application

### Using curl for Testing
To test the POST and GET methods on the facade service:
---
*__Test POST__*
curl -X POST -H "Content-Type: application/json" -d '{"msg": "Hello, facade!"}' http://localhost:5000/facade-service

*__Test GET__*
curl -X GET http://localhost:5000/facade-service

- The POST request should return a unique UUID.

- The GET request should return concatenated messages from both logging and message services.


---

## Console output:

![console](console_output.jpg?raw=true "Title")
