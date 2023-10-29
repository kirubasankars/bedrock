import re

from command_helper import *
from utils import *
import variables
import vault

def bootstrap_nomad():
    nomad_server = get_host_one('nomad_server')
    root_vault_token = variables.get_vault_token()

    result = command_remote(cmd=f"""
        source /opt/agent/profile
        nomad acl bootstrap -address='https://{nomad_server}:{const.NOMAD_PORT}'
    """, host=nomad_server)

    if result.returncode == 0:
        stdout = result.stdout.decode('utf-8')

        secret_id_line = re.sub(r'\s+', ' ', stdout.split("\n")[1])
        nomad_token = secret_id_line.split(" ")[3]

        vault_server = get_host_one('vault_server')
        nomad_server = get_host_one('nomad_server')

        command_remote(f"""
            source /opt/agent/profile
            export VAULT_TOKEN={root_vault_token}        
            
            vault policy write nomad-server /opt/agent/vault/config/nomad-integration-vault-policy.hcl            
            vault write /auth/token/roles/nomad-cluster @/opt/agent/vault/config/nomad-integration-vault-role.json

            vault write nomad/config/lease ttl=4h max_ttl=4h
            vault write nomad/config/access address='https://{nomad_server}:{const.NOMAD_PORT}' token='{nomad_token}'
            vault write nomad/role/management type=management global=true
        """, vault_server)

bootstrap_nomad()
