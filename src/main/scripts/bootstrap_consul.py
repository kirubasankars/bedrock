import re

from command_helper import *
from utils import *


def bootstrap_consul():
    consul_server = get_host_one("consul_server")

    result = command_remote("""
        source /opt/agent/profile
        consul acl bootstrap
    """, host=consul_server)

    if result.returncode == 0:
        secret_id_line = re.sub(r'\s+', ' ', result.stdout.decode('utf-8').split("\n")[1])
        consul_token = secret_id_line.split(" ")[1]

        with open("/workspace/cluster_config.env", "a") as f:
            f.write("\n")
            f.write(f"CONSUL_ADDRESS=https://{consul_server}:{const.CONSUL_HTTPS_PORT}\n")
            f.write(f"CONSUL_TOKEN={consul_token}\n")


bootstrap_consul()
