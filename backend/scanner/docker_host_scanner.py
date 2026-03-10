import docker


def scan_remote_docker(host_ip):

    try:

        client = docker.DockerClient(base_url=f"tcp://{host_ip}:2375")

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
                "host": host_ip
            })

        return results

    except Exception:

        return []
