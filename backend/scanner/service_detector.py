SERVICE_MAP = {
    "grafana": "grafana",
    "plex": "plex",
    "homeassistant": "homeassistant",
    "home-assistant": "homeassistant",
    "haos": "homeassistant",
    "nginx": "nginx",
    "postgres": "postgres",
    "mysql": "mysql",
    "mariadb": "mariadb",
    "redis": "redis",
    "mongo": "mongodb",
    "jellyfin": "jellyfin",
    "nextcloud": "nextcloud",
    "prometheus": "prometheus"
}

def detect_service(container):

    image = container.get("image", "").lower()
    name = container.get("name", "").lower()

    for key in SERVICE_MAP:

        if key in image or key in name:
            return SERVICE_MAP[key]

    return "docker"
