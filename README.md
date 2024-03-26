# Report Lab 1


## Application Structure

The Flask application is structured into three main components:

1. **Facade Service (`facade_service.py`):** Serves as the entry point for clients, aggregating data from the logging and message services.


2. **Logging Service (`logging_service.py`):** Logs messages received from the facade service.


3. **Messages Service (`messages_service.py`):** Provides a static message response.(not implemented)

## Setting Up

### Requirements

```sh
pip install Flask requests Flask-CORS
```

### Running the Services
Each service runs on its own port. I used separate terminal windows or sessions to start each service


### Testing the Application

### Using curl for Testing
To test the POST and GET methods on the facade service:

![console](console_output.jpg?raw=true "Title")
