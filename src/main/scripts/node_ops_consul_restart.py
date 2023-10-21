import wait_for_consul
from command_helper import *

command_remote(f"""
    /usr/bin/systemctl daemon-reload
    /usr/bin/systemctl restart consul;
""")

wait_for_consul.consul_up()
