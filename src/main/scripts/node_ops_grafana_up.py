from command_helper import *


def up():
    command_remote(f"""
        /usr/bin/systemctl daemon-reload
        /usr/bin/systemctl enable --now grafana
        /usr/bin/systemctl status grafana
    """)


if __name__ == "__main__":
    up()
