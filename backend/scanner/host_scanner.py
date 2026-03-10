import nmap


def scan_hosts(network="192.168.1.0/24"):

    nm = nmap.PortScanner()

    nm.scan(hosts=network, arguments="-sn")

    hosts = []

    for host in nm.all_hosts():

        hosts.append({
            "ip": host,
            "status": nm[host].state()
        })

    return hosts
