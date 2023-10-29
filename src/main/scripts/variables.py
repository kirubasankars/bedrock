import os

def get_cluster_id():
    return os.getenv("CLUSTER_ID", '')

def get_network_interface_name():
    return os.getenv("NETWORK_INTERFACE_NAME", '')

def get_vault_token():
    return os.getenv("VAULT_TOKEN", "")