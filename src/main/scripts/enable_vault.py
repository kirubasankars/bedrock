import sys

import vault
from utils import *
from variables import *

vault_server = get_host_one('vault_server')
root_vault_token = get_vault_token()

r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/auth/userpass",
                  json={"type": "userpass"},
                  verify=const.PUBLIC_CERT,
                  headers={'X-Vault-Token': root_vault_token})
r.raise_for_status()

r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/mounts/cluster_config",
                  json={"type": "kv-v2"},
                  verify=const.PUBLIC_CERT,
                  headers={'X-Vault-Token': root_vault_token})
r.raise_for_status()

r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/mounts/nomad",
                  json={"type": "nomad"},
                  verify=const.PUBLIC_CERT,
                  headers={'X-Vault-Token': root_vault_token})
r.raise_for_status()

r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/mounts/consul",
                  json={"type": "consul"},
                  verify=const.PUBLIC_CERT,
                  headers={'X-Vault-Token': root_vault_token})
r.raise_for_status()

vault.put_kv_cluster_config("nomad_integration_vault_token", {"token": root_vault_token})

