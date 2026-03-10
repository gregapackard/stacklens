# StackLens

<p align="center">
  <strong>Infrastructure Discovery & Dependency Mapping for Homelabs</strong>
</p>

<p align="center">
  Understand your infrastructure automatically.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-prototype-orange" />
  <img src="https://img.shields.io/badge/python-3.10+-blue" />
  <img src="https://img.shields.io/badge/license-TBD-lightgrey" />
</p>

---

## What is StackLens?

StackLens is a **self-hosted infrastructure discovery tool** designed for homelabs and self-hosted environments.

It automatically detects services running in your infrastructure and maps how they depend on each other.

Over time homelabs grow into complex systems of containers, services, databases, and networks. StackLens aims to provide a **live map of that infrastructure** so you can understand:

- what services are running  
- how they interact  
- what breaks if something fails  

Think of StackLens as **Google Maps for your homelab**.

---

## Example Infrastructure Map (Future Vision)

```
Proxmox
   │
Docker Host
   │
Mosquitto
   │
Zigbee2MQTT
   │
Home Assistant
```

StackLens will automatically detect and visualize relationships like this.

---

## Current Capabilities

StackLens is currently in **early prototype stage**.

Working features:

- FastAPI backend  
- Docker container discovery  
- Infrastructure scan API  

Example endpoint:

```
GET /scan/docker
```

Example response:

```
[
  {
    "name": "nginx",
    "image": ["nginx:latest"],
    "status": "running"
  }
]
```

---

## Planned Features

StackLens is designed to evolve into a full infrastructure intelligence platform.

Planned capabilities:

- Docker network discovery  
- Automatic service dependency detection  
- Infrastructure graph visualization  
- Failure impact simulation  
- Multi-host discovery  
- Proxmox environment discovery  
- AI-assisted infrastructure diagnostics  
- Plugin system for integrations  

---

## Installation (Prototype)

Clone the repository:

```
git clone https://github.com/gregapackard/stacklens.git
cd stacklens
```

Install dependencies:

```
pip install fastapi uvicorn docker networkx
```

Run the API server:

```
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open the API:

```
http://localhost:8000
```

---

## Project Vision

Modern homelabs resemble small data centers.

StackLens aims to provide:

- infrastructure visibility  
- automated discovery  
- service relationship mapping  
- operational insight  

The goal is to make it easy to understand **how your infrastructure actually works**.

---

## Contributing

Contributions are welcome once the project stabilizes.

Early development is currently focused on building the core infrastructure discovery engine.

---

## License

License will be determined as the project matures.
