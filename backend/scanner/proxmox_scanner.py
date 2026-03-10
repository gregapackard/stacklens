import os
from proxmoxer import ProxmoxAPI


def scan_proxmox():

    host = os.getenv("PROXMOX_HOST")
    token_name = os.getenv("PROXMOX_TOKEN_NAME")
    token_secret = os.getenv("PROXMOX_TOKEN_SECRET")

    # If no config exists, skip scanning
    if not host or not token_name or not token_secret:
        return []

    try:
        proxmox = ProxmoxAPI(
            host,
            user=token_name,
            token_name=token_name,
            token_value=token_secret,
            verify_ssl=False
        )

        nodes = proxmox.nodes.get()
        results = []

        for node in nodes:
            results.append({
                "type": "proxmox-node",
                "name": node["node"]
            })

        return results

    except Exception as e:
        print("Proxmox scan failed:", e)
        return []
