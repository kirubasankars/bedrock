from command_helper import *


def up():
    command_remote("""
        /usr/bin/systemctl daemon-reload
        /usr/bin/systemctl enable --now jenkins
        /usr/bin/systemctl status jenkins
        sh /opt/agent/jenkins/bin/install_plugins.sh    
    """)


if __name__ == "__main__":
    up()
