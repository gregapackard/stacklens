from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import subprocess

from backend.db import init_db
from backend.connectors_api import router as connectors_router

from backend.scanner.docker_scanner import scan_docker
from backend.scanner.proxmox_scanner import scan_proxmox
from backend.graph.graph_builder import build_graph

app = FastAPI(title="StackLens")

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")

app.include_router(connectors_router)


@app.on_event("startup")
def startup():

    init_db()


@app.get("/")
def root():

    return {
        "service": "StackLens",
        "status": "running"
    }


@app.get("/scan/docker")
def docker_scan():

    return scan_docker()


@app.get("/scan/proxmox")
def proxmox_scan():

    return scan_proxmox()


@app.get("/graph")
def graph():

    containers = scan_docker()
    proxmox_data = scan_proxmox()

    return build_graph(containers, proxmox_data)


@app.post("/docker/restart/{container}")
def restart_container(container: str):

    subprocess.run(["docker", "restart", container])

    return {"status": "restarted", "container": container}


@app.post("/docker/stop/{container}")
def stop_container(container: str):

    subprocess.run(["docker", "stop", container])

    return {"status": "stopped", "container": container}


@app.get("/docker/logs/{container}")
def container_logs(container: str):

    logs = subprocess.check_output(
        ["docker", "logs", "--tail", "50", container]
    ).decode()

    return {"logs": logs}
