def build_graph(containers, proxmox_data):

    nodes = []
    edges = []

    # Docker containers
    for c in containers:
        nodes.append({
            "id": f"docker-{c.get('id', c.get('name'))}",
            "label": c.get("name", "container"),
            "type": "docker"
        })

    # Proxmox VMs
    if isinstance(proxmox_data, dict):
        vms = proxmox_data.get("vms", [])
    else:
        vms = proxmox_data

    for vm in vms:
        nodes.append({
            "id": f"vm-{vm.get('vmid', vm.get('name'))}",
            "label": vm.get("name", "vm"),
            "type": "vm"
        })

    return {
        "nodes": nodes,
        "edges": edges
    }
