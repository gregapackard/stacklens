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
  <img src="https://img.shields.io/badge/self--hosted-homelab-green" />
  <img src="https://img.shields.io/badge/license-TBD-lightgrey" />
</p>

---

## What is StackLens?

StackLens is a **self-hosted infrastructure discovery and visualization tool** designed for homelabs and self-hosted environments.

It automatically detects services running in your infrastructure and maps how they relate to each other in a **live topology graph**.

Over time homelabs grow into complex systems of:

- containers  
- virtual machines  
- services  
- databases  
- automation platforms  
- networking layers  

StackLens helps you understand that complexity by providing a **visual map of your infrastructure**.

Think of StackLens as **Google Maps for your homelab**.

---

## Demo

<p align="center">
  <img src="docs/stacklens-ui.png" width="900">
</p>

---

## Current Capabilities

StackLens is currently in an **early prototype stage**, but several core features are already implemented.

### Infrastructure Discovery

- Docker container discovery
- Proxmox node discovery
- Proxmox VM detection
- Proxmox LXC detection
- Network service scanning

### Infrastructure Visualization

- Interactive topology graph
- Service icon detection
- Docker stack grouping

### Service Operations

From the UI you can:

- view container logs
- restart containers
- stop containers
- inspect service status

---

## Example Infrastructure Map (Vision)

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

StackLens aims to automatically discover and visualize relationships like this.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/gregapackard/stacklens.git
cd stacklens
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## Access the UI

Once running, open:

```
http://localhost/ui
```

or

```
http://<server-address>/ui
```

---

## Project Structure

```
backend/
  scanner/        infrastructure discovery engines
  graph/          graph construction logic
  main.py         FastAPI server

frontend/
  js/             graph rendering logic
  icons/          service icons
  index.html      UI
```

---

## Planned Features

StackLens is designed to evolve into a full **infrastructure intelligence platform**.

Planned capabilities include:

- Docker network discovery
- Automatic service dependency detection
- Failure impact simulation
- Multi-host discovery
- Kubernetes discovery
- Plugin system for integrations
- Infrastructure snapshots
- AI-assisted infrastructure diagnostics

---

## Contributing

Contributions are welcome once the project stabilizes.

Early development is focused on building the **core infrastructure discovery engine**.

---

## License

License will be determined as the project matures.
