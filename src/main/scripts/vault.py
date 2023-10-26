import requests

import const
import utils
import variables

def get_kv_cluster_config(path):
    vault_server = utils.get_host_one('vault_server')
    root_vault_token = variables.get_vault_token()
    try:
        r = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/cluster_config/data/{path}",
                         verify=const.PUBLIC_CERT,
                         headers={'X-Vault-Token': root_vault_token})
        return r.json()["data"]["data"]["token"]
    except Exception as e:
        pass
    return None
