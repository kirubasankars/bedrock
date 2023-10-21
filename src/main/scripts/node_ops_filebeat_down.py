from command_helper import *

command_remote(f"""
    /usr/bin/systemctl stop filebeat;
""")
