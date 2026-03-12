import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = {
    22: "ssh",
    80: "http",
    443: "https",
    2375: "docker",
    2376: "docker",
    3000: "grafana",
    8123: "homeassistant",
    9000: "portainer",
    8006: "proxmox",
    6443: "kubernetes"
}


def check_port(ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.4)

    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except:
        return False


def scan_host(ip):

    services = []

    for port, service in COMMON_PORTS.items():

        if check_port(ip, port):

            services.append({
                "service": service,
                "port": port
            })

    if services:

        host_type = "host"

        for s in services:
            if s["service"] == "proxmox":
                host_type = "proxmox"
            elif s["service"] == "docker":
                host_type = "docker"

        return {
            "ip": ip,
            "type": host_type,
            "services": services
        }

    return None


def scan_network(cidr):

    network = ipaddress.ip_network(cidr, strict=False)

    results = []

    with ThreadPoolExecutor(max_workers=64) as executor:

        futures = []

        for ip in network.hosts():
            futures.append(
                executor.submit(scan_host, str(ip))
            )

        for f in futures:

            result = f.result()

            if result:
                results.append(result)

    return results
