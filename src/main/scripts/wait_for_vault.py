import time

from cert import *
import requests
import const

def vault_up():
    vault_servers = get_vault_servers()
    consul_server = get_consul_server_0()

    retries = 50
    while True:
        try:
            r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/vault",
                             verify='/workspace/ca-public-key.pem')
            r.raise_for_status()
            data = r.json()
            if len([x for x in data if x["Status"] == "passing"]) == len(vault_servers):
                break
            print("Waiting for vault up ...", flush=True)
            time.sleep(10)
        except Exception as e:
            pass
        finally:
            retries = retries - 1
            if retries <= 0:
                raise Exception("vault boostrap error")

if __name__ == "__main__":
    vault_up()