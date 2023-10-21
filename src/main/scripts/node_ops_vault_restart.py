import unseal_vault
import wait_for_vault_sealed
from command_helper import *

command_remote(f"""
    /usr/bin/systemctl restart vault
    /usr/bin/systemctl status vault
""")

if __name__ == "__main__":
    wait_for_vault_sealed.vault_up()
    unseal_vault.unseal()
