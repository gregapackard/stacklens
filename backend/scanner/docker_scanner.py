import subprocess
import json


def get_container_stats():

    try:

        stats = subprocess.check_output([
            "docker",
            "stats",
            "--no-stream",
            "--format",
            "{{json .}}"
        ]).decode().strip().split("\n")

        parsed = {}

        for line in stats:
            data = json.loads(line)

            parsed[data["Name"]] = {
                "cpu": data["CPUPerc"],
                "mem": data["MemUsage"]
            }

        return parsed

    except:
        return {}


def scan_docker():

    containers = subprocess.check_output([
        "docker",
        "ps",
        "--format",
        "{{json .}}"
    ]).decode().strip().split("\n")

    stats = get_container_stats()

    results = []

    for c in containers:

        data = json.loads(c)

        name = data["Names"]

        results.append({

            "name": name,
            "image": data["Image"],
            "status": data["Status"],
            "networks": data["Networks"].split(","),
            "cpu": stats.get(name, {}).get("cpu"),
            "mem": stats.get(name, {}).get("mem")

        })

    return results
