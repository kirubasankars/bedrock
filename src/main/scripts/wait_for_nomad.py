import time

import requests

import const
from utils import *


def nomad_up():
    nomad_servers = get_nomad_servers()
    consul_server = get_consul_server_0()

    retries = 25
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/nomad",
                             verify=const.PUBLIC_CERT)
            r.raise_for_status()
            data = r.json()
            if len([x for x in data if x["Status"] == "passing"]) == len(nomad_servers) * 3:
                break
            print("Waiting for nomad up ...", flush=True)
            time.sleep(3)
        except Exception as e:
            pass
        finally:
            retries = retries - 1
            if retries <= 0:
                raise Exception("nomad bootstrap error")


if __name__ == "__main__":
    nomad_up()
