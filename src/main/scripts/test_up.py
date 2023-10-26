import requests

import const
from utils import *


def test_consul():
    nodes = flatten([get_host_list('consul_server'), get_host_list('consul_client')])
    for host in nodes:
        r = requests.get(f"https://{host}:{const.CONSUL_HTTPS_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_vault():
    vault_servers = get_host_list('vault_server')
    for host in vault_servers:
        r = requests.get(f"https://{host}:{const.VAULT_API_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_nomad():
    nodes = flatten([get_host_list('nomad_server'), get_host_list('nomad_client')])
    for host in nodes:
        r = requests.get(f"https://{host}:{const.NOMAD_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_vault_boostrap():
    if get_host_list('consul_server'):
        r = get_consul_health_check("vault")
        assert len(r) == len(get_host_list('vault_server'))


def test_consul_boostrap():
    r = get_consul_health_check("consul")
    assert len(r) == 0


def test_nomad_server_boostrap():
    r = get_consul_health_check("nomad")
    assert len(r) == len(get_host_list('nomad_server') * 3)


def test_nomad_client_boostrap():
    r = get_consul_health_check("nomad-client")
    assert len(r) == len(get_host_list('nomad_client'))
