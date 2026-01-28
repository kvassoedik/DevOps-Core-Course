# DevOps Info Service (Python)

## Overview
DevOps Info Service is a simple web application that provides information about itself and its runtime environment.  
The service exposes system details, runtime metrics, request metadata, and a health check endpoint that can be used for monitoring and orchestration tools.

This application serves as a foundation for future DevOps labs, including containerization, CI/CD pipelines, monitoring, and Kubernetes deployment.

---

## Prerequisites
- Python **3.11** or newer
- `pip` package manager

---

## Installation

Create and activate a virtual environment, then install dependencies:

### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
## Running the Application
Start the application with default settings:
```bash
python app.py
```
Run with custom configuration using environment variables:
```bash
HOST=127.0.0.1 PORT=3000 DEBUG=true python app.py
```
Once running, the service will be available at:
```bash
http://localhost:5000
```
or the custom port.

## API Endpoints
### Get /
Returns detailed information about:
- Service metadata
- System information
- Runtime and uptime
- Request metadata
- Available endpoints
Example:
```bash
curl http://127.0.0.1:5000/
```
Pretty-printed output:
```bash
curl -s http://127.0.0.1:5000/ | python -m json.tool
```
### GET /health
Health check endpoint used for monitoring and readiness/liveness probes.
Returns HTTP 200 if the service is healthy.
Example:
```bash
curl http://127.0.0.1:5000/health
```

## Configuration
| Variable | Default | Description |
|---|---|---|
| HOST | 0.0.0.0 | Address to bind the server |
| PORT | 5000 | Port to expose the service |
| DEBUG | False | Enable Flask debug mode | 
| LOG_LEVEL | INFO | Logging level | 
| SERVICE_NAME | devops-info-service | Service name | 
| SERVICE_VERSION | 1.0.0 | Service version | 
| SERVICE_DESCRIPTION | DevOps course info service | Service description | 