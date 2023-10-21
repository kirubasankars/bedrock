from command_helper import *
from utils import *
import const


def connect_vault_nomad():
    root_vault_token = get_vault_token()
    root_nomad_token = get_nomad_token()

    vault_server = get_vault_server_0()
    nomad_server = get_nomad_server_0()

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}        
                
        vault policy write nomad-server /opt/agent/vault/config/nomad-integration-vault-policy.hcl
        vault write /auth/token/roles/nomad-cluster @/opt/agent/vault/config/nomad-integration-vault-role.json
        
        vault write nomad/config/lease ttl=1h max_ttl=1h
        vault write nomad/config/access address='https://{nomad_server}:{const.NOMAD_PORT}' token='{root_nomad_token}'
        vault write nomad/role/management type=management global=true
    """, vault_server)

def connect_vault_consul():
    root_vault_token = get_vault_token()
    root_consul_token = get_consul_token()

    vault_server = get_vault_server_0()
    consul_server = get_consul_server_0()

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}        
        export CONSUL_HTTP_TOKEN={root_consul_token}
        
        consul acl policy create -name nomad-policy -rules @/opt/agent/vault/config/nomad-integration-consul-policy.hcl
        
        vault write consul/config/access address='https://{consul_server}:{const.CONSUL_HTTPS_PORT}' token="{root_consul_token}"
        vault write consul/roles/management policies=global-management ttl=1h
    """, vault_server)

def setup_vault_kv():
    root_vault_token = get_vault_token()
    root_consul_token = get_consul_token()

    vault_server = get_vault_server_0()
    consul_server = get_consul_server_0()
    encryption_key = get_encryption_key()

    r = requests.post(f"https://{vault_server}:{const.VAULT_API_PORT}/v1/auth/token/create-orphan",
                      json={"policies": ["nomad-server", "default"], "ttl": "72h", "renewable": True},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Vault-Token': root_vault_token})
    nomad_integration_vault_token = r.json()["auth"]["client_token"]

    r = requests.put(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/acl/token",
                      json={"Description": "nomad", "Policies": [{ "Name": "nomad-policy" }], "Local": False},
                      verify=const.PUBLIC_CERT,
                      headers={'X-Consul-Token': root_consul_token})

    nomad_integration_consul_token = r.json()["SecretID"]

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}            
        
        vault kv put -mount=cluster_config nomad_integration_vault_token token={nomad_integration_vault_token}
        vault kv put -mount=cluster_config nomad_integration_consul_token token={nomad_integration_consul_token}
        vault kv put -mount=cluster_config encryption_key key={encryption_key}
    """, vault_server)


connect_vault_consul()
connect_vault_nomad()
setup_vault_kv()
