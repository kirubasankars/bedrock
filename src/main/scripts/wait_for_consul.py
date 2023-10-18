import time
import requests
from cert import *

def consul_up():
    consul_servers = get_consul_servers()
    consul_clients = get_consul_clients()
    consul_server = get_consul_server_0()

    retries = 25
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/catalog/nodes", verify='/workspace/ca-public-key.pem')
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