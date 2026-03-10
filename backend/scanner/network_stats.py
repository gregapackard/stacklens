import subprocess

def get_bandwidth():

    try:

        output = subprocess.check_output(
            ["docker","stats","--no-stream","--format",
             "{{.Name}} {{.NetIO}}"]
        ).decode().splitlines()

        results = {}

        for line in output:

            parts = line.split()

            name = parts[0]
            rx = parts[1]

            rx = rx.replace("kB","").replace("B","")

            try:
                rx = float(rx)
            except:
                rx = 0

            results[name] = round(rx,2)

        return results

    except:
        return {}
