import re

from command_helper import *
from utils import *
import vault
import variables

def bootstrap_consul():
    consul_server = get_host_one("consul_server")
    root_vault_token = variables.get_vault_token()

    result = command_remote("""
        source /opt/agent/profile
        consul acl bootstrap
    """, host=consul_server)

    if result.returncode == 0:
        secret_id_line = re.sub(r'\s+', ' ', result.stdout.decode('utf-8').split("\n")[1])
        consul_token = secret_id_line.split(" ")[1]
        vault.put_kv_cluster_config("nomad_integration_consul_token", {"token": consul_token})

        vault_server = get_host_one('vault_server')
        consul_server = get_host_one("consul_server")

        command_remote(f"""
            source /opt/agent/profile
            export VAULT_TOKEN={root_vault_token}        
            export CONSUL_HTTP_TOKEN={consul_token}
                
            consul acl policy create -name nomad-policy -rules @/opt/agent/vault/config/nomad-integration-consul-policy.hcl            
            vault write consul/config/access address='https://{consul_server}:{const.CONSUL_HTTPS_PORT}' token="{consul_token}"
            vault write consul/roles/management policies=global-management ttl=4h
        """, vault_server)

bootstrap_consul()
