import time

from utils import *
from variables import *

def unseal():
    vault_servers = get_host_list('vault_server')
    if not os.path.isfile("/workspace/vault_unseal_tokens.txt"):
        return False

    with open("/workspace/vault_unseal_tokens.txt", "r") as f:
        unseal_keys = f.read().split("\n")[:3]

    root_vault_token = get_vault_token()

    for vault_server in vault_servers:

        for x in range(30):
            r = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/health", verify=const.PUBLIC_CERT)
            vault_health = r.json()
            print(vault_health, flush=True)
            if vault_health["initialized"] and vault_health["sealed"]:
                break
            time.sleep(10)

        requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/unseal",
                      json={"reset": True},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Vault-Token': root_vault_token})

        for unseal_key in unseal_keys:
            r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/unseal",
                              json={"key": unseal_key},
                              verify=const.PUBLIC_CERT,
                              headers={'X-Vault-Token': root_vault_token})
            print(r.text, r.json(), flush=True)
            r.raise_for_status()
            time.sleep(1)

        for x in range(30):
            r = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/health", verify=const.PUBLIC_CERT)
            vault_health = r.json()
            if vault_health["initialized"] and not vault_health["sealed"]:
                break
            time.sleep(10)

        time.sleep(15) # this allows vault to sync up

    return True


if __name__ == '__main__':
    unseal()
