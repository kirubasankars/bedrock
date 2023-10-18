import re

from utils import *
from command_helper import *


def bootstrap_consul():
    nodes = retrieve_host_ip_and_roles()
    consul_servers = [ip for ip, roles in nodes.items() if "consul_server" in roles]

    host = consul_servers[0]
    result = command_remote("/opt/agent/consul/bin/consul acl bootstrap", host=host)

    if result.returncode == 0:
        secret_id_line = re.sub(r'\s+', ' ', result.stdout.decode('utf-8').split("\n")[1])
        consul_token = secret_id_line.split(" ")[1]

        with open("/workspace/cluster_config.env", "a") as f:
            f.write("\n")
            f.write(f"CONSUL_ADDRESS=https://{host}:{const.CONSUL_HTTPS_PORT}\n")
            f.write(f"CONSUL_TOKEN={consul_token}\n")

bootstrap_consul()