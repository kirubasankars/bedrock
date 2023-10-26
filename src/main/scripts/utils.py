import os

import requests

import const

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


def retrieve_host_and_roles(host_filter=None):
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
        roles.extend(["telegraf", "filebeat"])
        if "nomad_client" in roles or "nomad_server" in roles or "vault_server" in roles or "jenkins" in roles:
            roles.append("consul_client")

        roles = list(set(roles))

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


def get_consul_health_check(service):
    consul_server = get_host_one("consul_server")
    r = requests.get(f"https://{consul_server}:{const.CONSUL_HTTPS_PORT}/v1/health/checks/{service}",
                     verify=const.PUBLIC_CERT)
    return r.json()

def get_host_one(role):
    hosts = retrieve_host_and_roles()
    filtered_hosts = [ip for ip, roles in hosts.items() if role in roles]
    if len(filtered_hosts) > 0:
        return filtered_hosts[0]

def get_host_list(role):
    hosts = retrieve_host_and_roles()
    return list(set([ip for ip, roles in hosts.items() if role in roles]))