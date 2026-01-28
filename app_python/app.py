"""
DevOps Info Service
A simple web service that exposes runtime and system information.
"""

import logging
import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, request

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("devops-info-service")


# Configuration (env vars)
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "False").strip().lower() == "true"

SERVICE_NAME = os.getenv("SERVICE_NAME", "devops-info-service")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
SERVICE_DESCRIPTION = os.getenv("SERVICE_DESCRIPTION", "DevOps course info service")
FRAMEWORK = "Flask"

# App start time for uptime
START_TIME_UTC = datetime.now(timezone.utc)

app = Flask(__name__)


def get_uptime() -> dict:
    """Return uptime in seconds and a human-friendly string."""
    delta = datetime.now(timezone.utc) - START_TIME_UTC
    seconds = int(delta.total_seconds())

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {
        "seconds": seconds,
        "human": f"{hours} hours, {minutes} minutes",
    }


def get_system_info() -> dict:
    """Collect system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.platform(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count() or 0,
        "python_version": platform.python_version(),
    }


def get_request_info() -> dict:
    """Collect request metadata (best-effort for client IP)."""
   
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.remote_addr

    return {
        "client_ip": client_ip,
        "user_agent": request.headers.get("User-Agent", ""),
        "method": request.method,
        "path": request.path,
    }


@app.get("/")
def index():
    """Main endpoint - service and system information."""
    logger.info("Request: %s %s", request.method, request.path)

    uptime = get_uptime()
    payload = {
        "service": {
            "name": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "description": SERVICE_DESCRIPTION,
            "framework": FRAMEWORK,
        },
        "system": get_system_info(),
        "runtime": {
            "uptime_seconds": uptime["seconds"],
            "uptime_human": uptime["human"],
            "current_time": datetime.now(timezone.utc).isoformat(),
            "timezone": "UTC",
        },
        "request": get_request_info(),
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Service information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
        ],
    }
    return jsonify(payload), 200


@app.get("/health")
def health():
    """Health check endpoint."""
    logger.info("Health check: %s %s", request.method, request.path)
    uptime = get_uptime()
    return (
        jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "uptime_seconds": uptime["seconds"],
            }
        ),
        200,
    )


@app.errorhandler(404)
def not_found(_error):
    return (
        jsonify({"error": "Not Found", "message": "Endpoint does not exist"}),
        404,
    )


@app.errorhandler(500)
def internal_error(_error):
    return (
        jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}),
        500,
    )


if __name__ == "__main__":
    logger.info("Starting %s on %s:%s (debug=%s)", SERVICE_NAME, HOST, PORT, DEBUG)
    app.run(host=HOST, port=PORT, debug=DEBUG)
