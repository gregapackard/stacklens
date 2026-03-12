from backend.scanner.service_detector import detect_service


# -------------------------
# Docker Stack Detection
# -------------------------

def get_stack_name(container_name):

    if "-" in container_name:
        return container_name.split("-")[0]

    return None


# -------------------------
# Graph Builder
# -------------------------

def build_graph(containers, proxmox_data):

    nodes = []
    edges = []

    node_id = 1

    docker_hosts = {}
    stack_nodes = {}
    prox_nodes = {}

    # -------------------------
    # Docker Hosts + Containers
    # -------------------------

    for container in containers:

        host = container.get("host", "docker")

        if host not in docker_hosts:

            docker_hosts[host] = node_id

            nodes.append({
                "id": node_id,
                "label": host,
                "type": "docker",
                "shape": "image",
                "image": "/ui/icons/docker.svg"
            })

            node_id += 1

        host_id = docker_hosts[host]

        name = container.get("name")
        stack = get_stack_name(name)

        parent_id = host_id

        # -------------------------
        # Stack grouping
        # -------------------------

        if stack:

            stack_key = f"{host}:{stack}"

            if stack_key not in stack_nodes:

                stack_nodes[stack_key] = node_id

                nodes.append({
                    "id": node_id,
                    "label": stack,
                    "type": "stack",
                    "shape": "image",
                    "image": "/ui/icons/docker.svg"
                })

                edges.append({
                    "id": f"{host_id}-{node_id}",
                    "from": host_id,
                    "to": node_id
                })

                node_id += 1

            parent_id = stack_nodes[stack_key]

        # -------------------------
        # Container Node
        # -------------------------

        service = detect_service(container)

        icon = f"/ui/icons/{service}.svg"

        nodes.append({
            "id": node_id,
            "label": name,
            "type": "container",
            "status": container.get("status"),
            "cpu": container.get("cpu"),
            "mem": container.get("mem"),
            "net": container.get("net"),
            "image": icon,
            "shape": "image"
        })

        edges.append({
            "id": f"{parent_id}-{node_id}",
            "from": parent_id,
            "to": node_id
        })

        node_id += 1

    # -------------------------
    # Proxmox Nodes
    # -------------------------

    for node in proxmox_data.get("nodes", []):

        prox_nodes[node["label"]] = node_id

        nodes.append({
            "id": node_id,
            "label": node["label"],
            "type": "proxmox",
            "image": "/ui/icons/proxmox.svg",
            "shape": "image"
        })

        node_id += 1

    # -------------------------
    # Proxmox VMs + LXCs
    # -------------------------

    for vm in proxmox_data.get("vms", []):

        host = vm.get("node")

        if host not in prox_nodes:
            continue

        host_id = prox_nodes[host]

        service = detect_service({
            "name": vm.get("label", ""),
            "image": ""
        })

        icon = f"/ui/icons/{service}.svg"

        if service == "docker":

            if vm.get("type") == "vm":
                icon = "/ui/icons/vm.svg"
            else:
                icon = "/ui/icons/docker.svg"

        nodes.append({
            "id": node_id,
            "label": vm.get("label"),
            "type": vm.get("type"),
            "status": vm.get("status"),
            "cpu": vm.get("cpu"),
            "mem": vm.get("mem"),
            "image": icon,
            "shape": "image"
        })

        edges.append({
            "id": f"{host_id}-{node_id}",
            "from": host_id,
            "to": node_id
        })

        node_id += 1

    return {
        "nodes": nodes,
        "edges": edges
    }
