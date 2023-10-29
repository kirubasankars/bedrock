from utils import *
from variables import *
import vault

def setup_vault_kv():
    root_vault_token = get_vault_token()

    vault_server = get_host_one('vault_server')
    r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/auth/token/create-orphan",
                      json={"policies": ["nomad-server", "default"], "ttl": "72h", "renewable": True},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Vault-Token': root_vault_token})
    nomad_integration_vault_token = r.json()["auth"]["client_token"]
    vault.put_kv_cluster_config("nomad_integration_vault_token", {"token": nomad_integration_vault_token})


    r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/auth/token/create-orphan",
                      json={"policies": ["prometheus-metrics"]},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Vault-Token': root_vault_token})
    prometheus_metrics_vault_token = r.json()["auth"]["client_token"]
    vault.put_kv_cluster_config("prometheus_metrics_vault_token", {"token": prometheus_metrics_vault_token})


    consul_server = get_host_one('consul_server')
    root_consul_token = vault.get_kv_cluster_config("nomad_integration_consul_token")
    r = requests.put(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/acl/token",
                      json={"Description": "nomad", "Policies": [{"Name": "nomad-policy"}], "Local": False},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Consul-Token': root_consul_token})

    nomad_integration_consul_token = r.json()["SecretID"]
    vault.put_kv_cluster_config("nomad_integration_consul_token", {"token": nomad_integration_consul_token})


setup_vault_kv()
