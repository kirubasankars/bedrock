import command_helper
from utils import *
import variables

def bootstrap2_vault():
    vault_server = get_host_one('vault_server')
    vault_token = variables.get_vault_token()

    command_helper.command_remote(f"""
        source /opt/agent/profile
        export VAULT_TOKEN={vault_token}
        vault auth enable userpass        
        vault secrets enable nomad
        vault secrets enable consul
        vault secrets enable -version=2 -path=cluster_config kv
    """, vault_server)

bootstrap2_vault()
