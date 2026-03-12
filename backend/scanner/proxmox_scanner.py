import requests
import sqlite3
import urllib3

urllib3.disable_warnings()

DB_PATH = "stacklens.db"


def get_connectors():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    rows = cur.execute(
        "SELECT host, username, token_name, token_secret, port FROM connectors WHERE type='proxmox'"
    ).fetchall()

    conn.close()

    connectors = []

    for r in rows:

        connectors.append({
            "host": r[0],
            "username": r[1],
            "token_name": r[2],
            "token_secret": r[3],
            "port": r[4] if r[4] else 8006
        })

    return connectors


def scan_proxmox():

    nodes = []
    vms = []

    connectors = get_connectors()

    for c in connectors:

        try:

            headers = {
                "Authorization": f"PVEAPIToken={c['username']}!{c['token_name']}={c['token_secret']}"
            }

            base = f"https://{c['host']}:{c['port']}/api2/json"

            node_data = requests.get(
                f"{base}/nodes",
                headers=headers,
                verify=False,
                timeout=5
            ).json()

            for node in node_data["data"]:

                node_name = node["node"]

                nodes.append({
                    "id": f"proxmox-{node_name}",
                    "label": node_name,
                    "type": "proxmox"
                })

                # -------------------------
                # QEMU Virtual Machines
                # -------------------------

                vm_data = requests.get(
                    f"{base}/nodes/{node_name}/qemu",
                    headers=headers,
                    verify=False,
                    timeout=5
                ).json()

                for vm in vm_data["data"]:

                    cpu = round(vm.get("cpu", 0) * 100, 2)

                    mem = round(vm.get("mem", 0) / 1024 / 1024, 2)
                    maxmem = round(vm.get("maxmem", 1) / 1024 / 1024, 2)

                    vms.append({
                        "id": f"vm-{vm['vmid']}",
                        "label": vm["name"],
                        "type": "vm",
                        "node": node_name,
                        "status": vm["status"],
                        "cpu": f"{cpu}%",
                        "mem": f"{mem}MB / {maxmem}MB",
                        "uptime": vm.get("uptime", 0)
                    })

                # -------------------------
                # LXC Containers
                # -------------------------

                lxc_data = requests.get(
                    f"{base}/nodes/{node_name}/lxc",
                    headers=headers,
                    verify=False,
                    timeout=5
                ).json()

                for ct in lxc_data["data"]:

                    cpu = round(ct.get("cpu", 0) * 100, 2)

                    mem = round(ct.get("mem", 0) / 1024 / 1024, 2)
                    maxmem = round(ct.get("maxmem", 1) / 1024 / 1024, 2)

                    vms.append({
                        "id": f"ct-{ct['vmid']}",
                        "label": ct["name"],
                        "type": "lxc",
                        "node": node_name,
                        "status": ct["status"],
                        "cpu": f"{cpu}%",
                        "mem": f"{mem}MB / {maxmem}MB",
                        "uptime": ct.get("uptime", 0)
                    })

        except Exception as e:
            print("Proxmox scan error:", e)

    return {
        "nodes": nodes,
        "vms": vms
    }
