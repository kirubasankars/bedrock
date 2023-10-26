from command_helper import *
from utils import *


def restart(name):
    command_local("""
        mkdir -p /opt/agent
        bash /scripts/rsync_remote_local.sh
    """)

    host = os.getenv("HOST")
    nodes = retrieve_host_and_roles()
    roles = nodes[host]

    if f"{name}" in roles or f"{name}_server" in roles:
        command_remote(f"""
            /usr/bin/systemctl restart {name};
        """)
    if f"{name}_client" in roles:
        command_remote(f"""
            sleep 15;
            /usr/bin/systemctl restart {name};
        """)


command = os.getenv("OPERATION")
restart(command.replace("_restart", ""))
