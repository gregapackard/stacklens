def build_graph(containers, proxmox_data):

    nodes = []
    edges = []

    # Proxmox node
    nodes.append({
        "id": "proxmox",
        "type": "proxmox"
    })

    for vm in proxmox_data.get("vms", []):

        vm_id = vm["name"]

        nodes.append({
            "id": vm_id,
            "type": "vm"
        })

        edges.append({
            "from": "proxmox",
            "to": vm_id
        })

    for c in containers:

        name = c["name"]

        nodes.append({
            "id": name,
            "type": "container",
            "image": c.get("image"),
            "status": c.get("status"),
            "cpu": c.get("cpu"),
            "mem": c.get("mem")
        })

        for net in c.get("networks", []):

            nodes.append({
                "id": net,
                "type": "network"
            })

            edges.append({
                "from": name,
                "to": net
            })

    # remove duplicate nodes
    unique = {}
    for n in nodes:
        unique[n["id"]] = n

    return {
        "nodes": list(unique.values()),
        "edges": edges
    }
