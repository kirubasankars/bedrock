from command_helper import *


def up():
    command_remote("""
        /usr/bin/systemctl daemon-reload
        /usr/bin/systemctl enable --now filebeat
        /usr/bin/systemctl status filebeat
    """)


if __name__ == "__main__":
    up()
