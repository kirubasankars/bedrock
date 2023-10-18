from command_helper import *

def up():
    command_remote(f"""
        /usr/bin/systemctl enable --now vault
        /usr/bin/systemctl status vault
    """)

if __name__ == "__main__":
    up()