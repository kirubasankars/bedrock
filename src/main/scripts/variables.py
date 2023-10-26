import os

def get_cluster_id():
    return os.getenv("CLUSTER_ID", '')


def get_network_interface_name():
    return os.getenv("NETWORK_INTERFACE_NAME", '')


def get_encryption_key():
    return os.getenv("ENCRYPTION_KEY", '')


def get_prometheus_admin_password_hash():
    return os.getenv("PROMETHEUS_ADMIN_PASSWORD_HASH", "")


def get_consul_token():
    return os.getenv("CONSUL_TOKEN", "")


def get_vault_token():
    return os.getenv("VAULT_TOKEN", "")


def get_nomad_token():
    return os.getenv("NOMAD_TOKEN", "")
