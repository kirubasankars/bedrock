import bcrypt
from cert import *
from utils import *

def main():

    generate_ca_private()
    generate_ca_public(get_cluster_id())

    with open(f"/workspace/cluster_config.env", "w") as f:
        f.writelines(f"CLUSTER_ID={get_cluster_id()}\n")
        f.writelines(f"ENCRYPTION_KEY={generate_encryption_key()}\n")

main()