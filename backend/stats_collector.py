import docker
import threading
import time

client = docker.from_env()

# in-memory cache
stats_cache = {}

def collect_stats():

    global stats_cache

    while True:

        new_cache = {}

        try:

            containers = client.containers.list()

            for c in containers:

                try:

                    s = c.stats(stream=False)

                    cpu_delta = s["cpu_stats"]["cpu_usage"]["total_usage"] - \
                                s["precpu_stats"]["cpu_usage"]["total_usage"]

                    system_delta = s["cpu_stats"]["system_cpu_usage"] - \
                                   s["precpu_stats"]["system_cpu_usage"]

                    cpu_percent = 0.0

                    if system_delta > 0 and cpu_delta > 0:
                        cpu_percent = (cpu_delta / system_delta) * \
                                      len(s["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100

                    mem_usage = s["memory_stats"]["usage"]
                    mem_limit = s["memory_stats"]["limit"]

                    net_rx = 0
                    net_tx = 0

                    for iface in s["networks"].values():
                        net_rx += iface["rx_bytes"]
                        net_tx += iface["tx_bytes"]

                    new_cache[c.name] = {
                        "cpu": f"{round(cpu_percent,2)}%",
                        "mem": f"{round(mem_usage/1024/1024,2)}MB / {round(mem_limit/1024/1024,2)}MB",
                        "net_rx": net_rx,
                        "net_tx": net_tx
                    }

                except Exception:
                    continue

            stats_cache = new_cache

        except Exception:
            pass

        time.sleep(2)


def start_collector():

    thread = threading.Thread(target=collect_stats, daemon=True)
    thread.start()


def get_stats():

    return stats_cache
