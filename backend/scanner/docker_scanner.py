import docker

def scan_docker():

    client = docker.from_env()

    containers = client.containers.list()

    results = []

    for c in containers:

        results.append({
            "name": c.name,
            "image": c.image.tags,
            "status": c.status
        })

    return results
