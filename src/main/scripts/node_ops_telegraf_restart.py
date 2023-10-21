from command_helper import *

command_remote(f"""
    /usr/bin/systemctl daemon-reload
    /usr/bin/systemctl restart telegraf;
""")
