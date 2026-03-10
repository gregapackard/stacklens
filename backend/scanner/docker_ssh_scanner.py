import paramiko
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

user = os.getenv("SSH_USER")
key_path = os.getenv("SSH_KEY_PATH")


def scan_single_host(host):

    results = []

    try:

        key = paramiko.Ed25519Key.from_private_key_file(key_path)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host, username=user, pkey=key, timeout=3)

        stdin, stdout, stderr = ssh.exec_command(
            "docker ps --format '{{.Names}} {{.Image}} {{.Status}}'"
        )

        output = stdout.read().decode()

        for line in output.splitlines():

            parts = line.split(" ", 2)

            if len(parts) >= 3:

                results.append({
                    "name": parts[0],
                    "image": parts[1],
                    "status": parts[2],
                    "host": host
                })

        ssh.close()

    except Exception:
        pass

    return results


def scan_remote_docker(hosts):

    all_results = []

    with ThreadPoolExecutor(max_workers=20) as executor:

        futures = [executor.submit(scan_single_host, h) for h in hosts]

        for f in futures:

            all_results.extend(f.result())

    return all_results
