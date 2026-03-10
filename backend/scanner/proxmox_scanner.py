import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

load_dotenv()


def scan_proxmox():

    host = os.getenv("PROXMOX_HOST")
    user = os.getenv("PROXMOX_USER")
    token_name = os.getenv("PROXMOX_TOKEN_NAME")
    token_secret = os.getenv("PROXMOX_TOKEN_SECRET")

    proxmox = ProxmoxAPI(
        host,
        user=user,
        token_name=token_name,
        token_value=token_secret,
        verify_ssl=False
    )

    nodes = []
    vms = []
    lxcs = []

    for node in proxmox.nodes.get():

        node_name = node["node"]
        nodes.append(node_name)

        for vm in proxmox.nodes(node_name).qemu.get():

            vms.append({
                "name": vm["name"],
                "vmid": vm["vmid"],
                "status": vm["status"],
                "node": node_name,
                "type": "vm"
            })

        for ct in proxmox.nodes(node_name).lxc.get():

            lxcs.append({
                "name": ct["name"],
                "vmid": ct["vmid"],
                "status": ct["status"],
                "node": node_name,
                "type": "lxc"
            })

    return {
        "nodes": nodes,
        "vms": vms,
        "lxcs": lxcs
    }
