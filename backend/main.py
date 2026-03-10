from fastapi import FastAPI
from backend.scanner.docker_scanner import scan_docker

app = FastAPI(title="StackLens")

@app.get("/")
def root():
    return {
        "service": "StackLens",
        "status": "running"
    }

@app.get("/scan/docker")
def docker_scan():
    return scan_docker()
