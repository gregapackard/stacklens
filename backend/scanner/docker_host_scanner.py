import docker


def scan_remote_docker(host_ip, port=2375):

    try:

        client = docker.DockerClient(
            base_url=f"tcp://{host_ip}:{port}",
            timeout=3
        )

        containers = client.containers.list(all=True)

        results = []

        for c in containers:

            image_name = ""

            if c.image.tags:
                image_name = c.image.tags[0]
            else:
                image_name = c.image.short_id

            results.append({
                "name": c.name,
                "image": image_name,
                "status": c.status,
                "host": host_ip
            })

        return results

    except Exception:

        return []
