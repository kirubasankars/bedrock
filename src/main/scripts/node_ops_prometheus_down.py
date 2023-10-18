from command_helper import *
from utils import *

command_remote(f"""
    /usr/bin/systemctl stop prometheus;
""")