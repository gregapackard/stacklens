from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import subprocess
import requests
import sqlite3

from backend.db import init_db
from backend.connectors_api import router as connectors_router

from backend.scanner.docker_scanner import scan_docker
from backend.scanner.proxmox_scanner import scan_proxmox
from backend.scanner.discovery_scanner import scan_network

from backend.graph.graph_builder import build_graph

app = FastAPI(title="StackLens")


# -------------------------
# Static UI
# -------------------------

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")


# -------------------------
# Connector API
# -------------------------

app.include_router(connectors_router)


# -------------------------
# Startup
# -------------------------

@app.on_event("startup")
def startup():
    init_db()


# -------------------------
# Root
# -------------------------

@app.get("/")
def root():
    return {
        "service": "StackLens",
        "status": "running"
    }


# -------------------------
# Settings Page
# -------------------------

@app.get("/settings")
def settings():
    return FileResponse("frontend/settings.html")


# -------------------------
# Discovery Scanner
# -------------------------

@app.get("/discover")
def discover():

    network = "192.168.1.0/24"

    results = scan_network(network)

    return {
        "network": network,
        "discovered": results
    }


# -------------------------
# Manual Scanners
# -------------------------

@app.get("/scan/docker")
def docker_scan():
    return scan_docker()


@app.get("/scan/proxmox")
def proxmox_scan():
    return scan_proxmox()


# -------------------------
# Graph
# -------------------------

@app.get("/graph")
def graph():

    containers = scan_docker()
    proxmox_data = scan_proxmox()

    return build_graph(containers, proxmox_data)


# -------------------------
# Docker Controls
# -------------------------

@app.post("/docker/restart/{container}")
def restart_container(container: str):

    subprocess.run(["docker", "restart", container])

    return {
        "status": "restarted",
        "container": container
    }


@app.post("/docker/stop/{container}")
def stop_container(container: str):

    subprocess.run(["docker", "stop", container])

    return {
        "status": "stopped",
        "container": container
    }


@app.get("/docker/logs/{container}")
def container_logs(container: str):

    logs = subprocess.check_output(
        ["docker", "logs", "--tail", "50", container]
    ).decode()

    return {
        "logs": logs
    }


# -------------------------
# Docker Stats (restored)
# -------------------------

@app.get("/docker/stats/{container}")
def docker_stats(container: str):

    import docker

    client = docker.from_env()

    try:

        c = client.containers.get(container)
        s = c.stats(stream=False)

        cpu_delta = s["cpu_stats"]["cpu_usage"]["total_usage"] - \
                    s["precpu_stats"]["cpu_usage"]["total_usage"]

        system_delta = s["cpu_stats"]["system_cpu_usage"] - \
                       s["precpu_stats"]["system_cpu_usage"]

        cpu_percent = 0.0

        if system_delta > 0 and cpu_delta > 0:

            cpu_percent = (
                cpu_delta /
                system_delta *
                len(s["cpu_stats"]["cpu_usage"]["percpu_usage"])
            ) * 100

        mem_usage = s["memory_stats"]["usage"]
        mem_limit = s["memory_stats"]["limit"]

        net_rx = 0
        net_tx = 0

        if "networks" in s:
            for iface in s["networks"].values():
                net_rx += iface.get("rx_bytes", 0)
                net_tx += iface.get("tx_bytes", 0)

        return {
            "cpu": f"{round(cpu_percent,2)}%",
            "mem": f"{round(mem_usage/1024/1024,2)}MB / {round(mem_limit/1024/1024,2)}MB",
            "net": f"{round(net_rx/1024/1024,2)}MB RX / {round(net_tx/1024/1024,2)}MB TX",
            "disk": "0MB Read / 0MB Write"
        }

    except Exception as e:

        return {
            "error": str(e)
        }
