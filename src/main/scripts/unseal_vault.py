import time

from command_helper import *
from utils import *


def unseal():
    nodes = retrieve_host_ip_and_roles()
    vault_servers = [ip for ip, roles in nodes.items() if "vault_server" in roles]
    if not os.path.isfile("/workspace/vault_unseal_tokens.txt"):
        return False

    with open("/workspace/vault_unseal_tokens.txt", "r") as f:
        unseal_keys = f.read().split("\n")[:3]

    root_vault_token = get_vault_token()

    for vault_server in vault_servers:

        r = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/health", verify=const.PUBLIC_CERT)
        vault_health = r.json()

        if vault_health["initialized"] and vault_health["sealed"]:

            requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/unseal",
                          json={"reset": True},
                          verify=const.PUBLIC_CERT,
                          headers={'X-Vault-Token': root_vault_token})

            for unseal_key in unseal_keys:
                r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/unseal",
                                  json={"key": unseal_key},
                                  verify=const.PUBLIC_CERT,
                                  headers={'X-Vault-Token': root_vault_token})
                r.raise_for_status()
                time.sleep(1)

            vault_health = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/health",
                                        verify=const.PUBLIC_CERT).json()
            assert vault_health["initialized"] and not vault_health["sealed"]

    return True


if __name__ == '__main__':
    unseal()
