import docker

client = docker.from_env()


def scan_docker():

    containers = client.containers.list()

    results = []

    for c in containers:

        image_name = ""

        if c.image.tags:
            image_name = c.image.tags[0]

        results.append({
            "name": c.name,
            "image": image_name,
            "status": c.status,
            "cpu": "-",
            "mem": "-",
            "host": "localhost"
        })

    return results
