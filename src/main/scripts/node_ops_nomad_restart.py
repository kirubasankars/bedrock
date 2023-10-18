from command_helper import *
import wait_for_nomad

command_remote(f"""
    /usr/bin/systemctl daemon-reload
    /usr/bin/systemctl restart nomad;
""")

wait_for_nomad.nomad_up()