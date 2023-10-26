import time

import requests

import const
from utils import *


def nomad_up():
    nomad_clients = get_host_list('nomad_client')
    consul_server = get_host_one("consul_server")

    retries = 25
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/nomad-client",
                             verify=const.PUBLIC_CERT)
            r.raise_for_status()
            data = r.json()
            if len([x for x in data if x["Status"] == "passing"]) == len(nomad_clients):
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
