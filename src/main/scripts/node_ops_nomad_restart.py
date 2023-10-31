import wait_for_nomad_server
import wait_for_nomad_client
from command_helper import *

command_remote(f"""
    /usr/bin/systemctl daemon-reload
    /usr/bin/systemctl restart nomad;
""")

wait_for_nomad_server.nomad_up()
wait_for_nomad_client.nomad_up()