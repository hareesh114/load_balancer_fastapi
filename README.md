# Load Balancer (FastAPI)

## Features
- Round Robin Load Balancing
- Supports GET & POST
- JWT header forwarding
- Redirect handling

## Architecture

Client → FastAPI Load Balancer → Django Servers (8001, 8002, 8003)

## Run

uvicorn load_balancer:app --port 8000 --reload