import re

from command_helper import *
from utils import *


def bootstrap_nomad():
    nomad_server = get_nomad_server_0()

    result = command_remote(cmd=f"""
    source /opt/agent/profile
    nomad acl bootstrap -address='https://{nomad_server}:{const.NOMAD_PORT}'
""", host=nomad_server)
    if result.returncode == 0:
        stdout = result.stdout.decode('utf-8')

        secret_id_line = re.sub(r'\s+', ' ', stdout.split("\n")[1])
        nomad_token = secret_id_line.split(" ")[3]

        with open("/workspace/cluster_config.env", "a") as f:
            f.write("\n")
            f.write(f"NOMAD_ADDRESS=https://{nomad_server}:{const.NOMAD_PORT}\n")
            f.write(f"NOMAD_TOKEN={nomad_token}\n")


bootstrap_nomad()
