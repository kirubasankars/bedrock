from command_helper import *
from utils import *
import const


def connect_vault_nomad():
    root_vault_token = os.getenv("VAULT_TOKEN", "")
    root_nomad_token = os.getenv("NOMAD_TOKEN", "")

    vault_servers = [ip for ip, roles in retrieve_host_ip_and_roles().items() if "vault_server" in roles]
    host = vault_servers[0]

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}        
                
        vault policy write nomad-server /opt/agent/vault/config/nomad-server-policy.hcl
        vault write /auth/token/roles/nomad-cluster @/opt/agent/vault/config/nomad-cluster-role.json
        
        vault write nomad/config/lease ttl=1h max_ttl=1h
        vault write nomad/config/access address='https://{host}:{const.NOMAD_PORT}' token='{root_nomad_token}'
        vault write nomad/role/management type=management global=true
    """, host)


def connect_vault_consul():
    root_vault_token = os.getenv("VAULT_TOKEN", "")
    root_consul_token = os.getenv("CONSUL_TOKEN", "")

    vault_servers = [ip for ip, roles in retrieve_host_ip_and_roles().items() if "vault_server" in roles]
    host = vault_servers[0]

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}        
                
        vault write consul/config/access address='https://{host}:{const.CONSUL_HTTPS_PORT}' token="{root_consul_token}"
        vault write consul/roles/management policies=global-management ttl=1h
    """, host)


def setup_vault_kv():
    root_vault_token = os.getenv("VAULT_TOKEN", "")
    root_nomad_token = os.getenv("NOMAD_TOKEN", "")
    root_consul_token = os.getenv("CONSUL_TOKEN", "")

    vault_servers = [ip for ip, roles in retrieve_host_ip_and_roles().items() if "vault_server" in roles]
    host = vault_servers[0]
    encryption_key = get_encryption_key()

    command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={root_vault_token}            
        
        vault kv put -mount=cluster_config nomad_token token={root_nomad_token}
        vault kv put -mount=cluster_config consul_token token={root_consul_token}
        vault kv put -mount=cluster_config vault_token token={root_vault_token}        
        vault kv put -mount=cluster_config encryption_key key={encryption_key}        
    """, host)


setup_vault_kv()
connect_vault_consul()
connect_vault_nomad()