import requests
import utils
import const
import variables

def get_consul_management_token():
    vault_server = utils.get_host_one("vault_server")
    root_vault_token = variables.get_vault_token()

    r = requests.get(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/consul/creds/management",
                     verify=const.PUBLIC_CERT,
                     headers={'X-Vault-Token': root_vault_token})

    r = r.json()
    print(r)
    return r["data"]["token"]