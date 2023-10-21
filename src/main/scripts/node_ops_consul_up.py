from command_helper import *


def up():
    command_remote("""
        /usr/bin/systemctl daemon-reload
        /usr/bin/systemctl restart systemd-resolved
        /usr/bin/systemctl enable --now consul
        /usr/bin/systemctl status consul
    """)


if __name__ == "__main__":
    up()
