import json

import vault
import cert
from utils import *
from variables import *

vault_server = get_host_one('vault_server')
root_vault_token = get_vault_token()

def update_kv_policy():
    with open("/agent/vault/config/kv-admin-policy.hcl") as f:
        policy = f.read()
    url = f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/policy/kv-admin-policy"
    r = requests.post(url, verify=const.PUBLIC_CERT, headers={'X-Vault-Token': root_vault_token}, json={"policy": policy})
    r.raise_for_status()

def update_prometheus_policy():
    with open("/agent/vault/config/prometheus-metrics.hcl") as f:
        policy = f.read()
    url = f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/policy/prometheus-metrics"
    r = requests.post(url, verify=const.PUBLIC_CERT, headers={'X-Vault-Token': root_vault_token}, json={"policy": policy})
    r.raise_for_status()

def update_nomad_integration_policy():
    with open("/agent/vault/config/nomad-integration-vault-policy.hcl") as f:
        policy = f.read()
    url = f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/policy/nomad-integration-vault-policy"
    r = requests.post(url, verify=const.PUBLIC_CERT, headers={'X-Vault-Token': root_vault_token}, json={"policy": policy})
    r.raise_for_status()

def update_nomad_integration_role():
    with open("/agent/vault/config/nomad-integration-vault-role.json") as f:
        role = f.read()
    url = f"https://{vault_server}:{const.VAULT_API_PORT}/v1/sys/role/nomad-integration-vault-role"
    r = requests.post(url, verify=const.PUBLIC_CERT, headers={'X-Vault-Token': root_vault_token}, json=json.loads(role))
    r.raise_for_status()

update_kv_policy()
update_nomad_integration_policy()
update_prometheus_policy()
#update_nomad_integration_role()
#TODO: consul policy

vault.put_kv_cluster_config("encryption_key", {"key": cert.generate_encryption_key()})