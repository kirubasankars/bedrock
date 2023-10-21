import time

import requests

import const
from utils import *


def vault_up():
    vault_servers = get_vault_servers()
    consul_server = get_consul_server_0()

    retries = 25
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/vault",
                             verify=const.PUBLIC_CERT)
            r.raise_for_status()
            if len(r.json()) == len(vault_servers):
                break
            time.sleep(3)
        finally:
            retries = retries - 1
            if retries <= 0:
                break


if __name__ == "__main__":
    vault_up()
