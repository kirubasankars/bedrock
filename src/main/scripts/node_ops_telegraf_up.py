from command_helper import *

def up():
    command_remote(f"""
        /usr/bin/systemctl daemon-reload
        /usr/bin/systemctl enable --now telegraf
        /usr/bin/systemctl status telegraf
    """)

if __name__ == "__main__":
    up()