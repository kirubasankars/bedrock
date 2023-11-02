import re

import command_helper
from utils import *
import variables
import vault

def bootstrap_consul():
    consul_server = get_host_one("consul_server")
    vault_server = get_host_one('vault_server')
    vault_token = variables.get_vault_token()

    result = command_helper.command_remote("""
        source /opt/agent/profile
        consul acl bootstrap
    """, host=consul_server)

    if result.returncode == 0:
        secret_id_line = re.sub(r'\s+', ' ', result.stdout.decode('utf-8').split("\n")[1])
        consul_token = secret_id_line.split(" ")[1]

        command_helper.command_remote(f"""
            source /opt/agent/profile
            export VAULT_TOKEN={vault_token}        
            export CONSUL_HTTP_TOKEN={consul_token}

            consul acl policy create -name nomad-policy -rules @/opt/agent/vault/config/nomad-integration-consul-policy.hcl
            vault write consul/config/access address='https://{consul_server}:{const.CONSUL_HTTPS_PORT}' token="{consul_token}"
            vault write consul/roles/management policies=global-management ttl=4h
        """, vault_server)

bootstrap_consul()
