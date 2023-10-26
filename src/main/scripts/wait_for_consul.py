import time

from utils import *


def consul_up():
    consul_servers = get_host_list('consul_server')
    consul_clients = get_host_list('consul_client')
    consul_server = get_host_one("consul_server")

    retries = 25
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/catalog/nodes",
                             verify=const.PUBLIC_CERT)
            r.raise_for_status()
            if len(r.json()) == len(consul_servers + consul_clients):
                break
            print("Waiting for consul up ...", flush=True)
            time.sleep(3)
        except Exception as e:
            pass
        finally:
            retries = retries - 1
            if retries <= 0:
                break


if __name__ == "__main__":
    consul_up()
