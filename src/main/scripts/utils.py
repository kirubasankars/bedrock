import os
import const
import requests

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

def custom_sort_order(element):
    custom_order_list = [
        'telegraf',
        'prometheus',
        'vault_server',
        'consul_server',
        'nomad_server',
        'consul_client',
        'nomad_client',
        'jenkins'
    ]
    if element in custom_order_list:
        return custom_order_list.index(element)
    else:
        return 99

def retrieve_host_ip_and_roles(host_filter = None):
    with open("/workspace/hosts.txt", "r") as f:
        filedata = f.read()
    lines = [x.strip() for x in filedata.split("\n") if x.strip()]
    nodes = {}
    for line in lines:
        s = line.split(" ")
        if len(s) == 2:
            nodes[s[0]] = s[1].split(",")
        if len(s) == 1:
            nodes[s[0]] = []

    for host, roles in nodes.items():
        roles.extend(["telegraf", "filebeat", "consul_client", "cluster"])
        roles = list(set(roles))

        if "consul_server" in roles or "jenkins" in roles:
            roles.remove("consul_client")

        if "jenkins" in roles:
            roles.remove("cluster")

        nodes[host] = sorted(roles, key=custom_sort_order)

    nomad_servers = [ip for ip, roles in nodes.items() if "nomad_server" in roles]
    consul_servers = [ip for ip, roles in nodes.items() if "consul_server" in roles]
    vault_servers = [ip for ip, roles in nodes.items() if "vault_server" in roles]

    assert len(nomad_servers) == 1 or len(nomad_servers) == 3
    assert len(consul_servers) == 1 or len(consul_servers) == 3
    assert len(vault_servers) == 1 or len(vault_servers) == 3

    if host_filter:
        nodes = {host: roles for host, roles in nodes.items() if set(host_filter) & set(roles)}

    return nodes

def get_vault_servers():
    nodes = retrieve_host_ip_and_roles()
    return [ip for ip, roles in nodes.items() if "vault_server" in roles ]

def get_vault_server_0():
    vault_servers = get_vault_servers()
    if len(vault_servers) > 0:
        return vault_servers[0]

def get_nomad_servers():
    nodes = retrieve_host_ip_and_roles()
    return [ip for ip, roles in nodes.items() if "nomad_server" in roles ]

def get_nomad_clients():
    nodes = retrieve_host_ip_and_roles()
    return [ip for ip, roles in nodes.items() if "nomad_client" in roles ]

def get_nomad_server_0():
    nomad_servers = get_nomad_servers()
    if len(nomad_servers) > 0:
        return nomad_servers[0]

def get_consul_servers():
    nodes = retrieve_host_ip_and_roles()
    return [ip for ip, roles in nodes.items() if "consul_server" in roles ]

def get_consul_clients():
    nodes = retrieve_host_ip_and_roles()
    return [ip for ip, roles in nodes.items() if "consul_client" in roles ]

def get_consul_server_0():
    consul_servers = get_consul_servers()
    if len(consul_servers) > 0:
        return consul_servers[0]

def get_jenkins_node_0():
    nodes = retrieve_host_ip_and_roles()
    jenkins = [ip for ip, roles in nodes.items() if "jenkins" in roles ]
    if len(jenkins) > 0:
        return jenkins[0]

def flatten(nested_list):
    flat_list = []
    stack = [nested_list]

    while stack:
        current_element = stack.pop()

        if isinstance(current_element, list):
            stack.extend(reversed(current_element))
        else:
            flat_list.append(current_element)

    return list(reversed(flat_list))

def get_consul_health_check(service):
    consul_server = get_consul_server_0()
    r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/{service}",
                     verify='/workspace/ca-public-key.pem')
    return r.json()