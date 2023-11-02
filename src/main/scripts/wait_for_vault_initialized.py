import sys
import time

import requests

import const
from utils import *


def vault_up():
    consul_server = get_host_one("consul_server")

    retries = 50
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/vault",
                             verify=const.PUBLIC_CERT)
            r.raise_for_status()
            if len([x for x in r.json() if "initialized" in x["ServiceTags"]]) == 1:
                break
            print("waiting for vault initialized and active status", flush=True)
        finally:
            retries = retries - 1
            if retries <= 0:
                sys.exit(1)
            time.sleep(15)

if __name__ == "__main__":
    vault_up()
