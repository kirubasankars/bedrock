from utils import *
from cert import *
import wait_for_vault_initialized
def bootstrap_vault():
    vault_server = get_host_one('vault_server')

    result = command_remote(f"""
        source /opt/agent/profile
        vault operator init -address='https://{vault_server}:{const.VAULT_API_PORT}'
    """, host=vault_server)

    if result.returncode == 0:
        stdout = result.stdout.decode('utf-8')

        vault_token = (stdout.split("\n")[6]).split(" ")[3]

        with open("/workspace/vault_token.txt", "a") as f:
            f.write(f"{vault_token}")

        with open("/workspace/vault_unseal_tokens.txt", "w") as f:
            for x in stdout.split("\n")[:5]:
                f.write(x.split(" ")[3] + "\n")

    wait_for_vault_initialized.vault_up()

bootstrap_vault()
