# StackLens

StackLens is a self-hosted infrastructure discovery and dependency mapping tool designed for homelabs and self-hosted environments.

It automatically discovers services running on your infrastructure and maps how they depend on each other.

The goal is to provide visibility into complex homelab environments where multiple services interact across containers, VMs, and networks.

---

## Features (Planned)

- Automatic Docker container discovery
- Service dependency detection
- Infrastructure graph visualization
- Failure impact simulation
- AI-assisted infrastructure diagnostics
- Proxmox environment discovery

---

## Why StackLens?

Homelabs grow quickly.

After a while it becomes difficult to answer questions like:

- What breaks if this container stops?
- Which services depend on this database?
- What infrastructure is actually running?

StackLens aims to solve that by creating a live map of your infrastructure.

Think of it as **Google Maps for your homelab**.

---

## Current Status

Early prototype.

Current capabilities:

- FastAPI backend
- Docker container discovery
- API endpoint for infrastructure scanning

---

## Example API

Docker discovery endpoint:

GET /scan/docker

Example response:

[
  {
    "name": "nginx",
    "image": ["nginx:latest"],
    "status": "running"
  }
]

---

## Roadmap

Planned features:

- Docker network discovery
- Automatic dependency graph generation
- Web-based infrastructure visualization
- Failure simulation engine
- Multi-host discovery
- Plugin system

---

## Installation (Prototype)

Clone the repository:

git clone https://github.com/gregapackard/stacklens.git  
cd stacklens

Install dependencies:

pip install fastapi uvicorn docker networkx

Run the API server:

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

Open:

http://localhost:8000

---

## Long Term Vision

StackLens aims to become a powerful infrastructure intelligence tool for self-hosted environments, helping operators understand and manage complex service relationships automatically.

---

## License

License will be determined as the project matures.
