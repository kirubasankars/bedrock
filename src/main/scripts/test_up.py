import requests

import const
from utils import *


def test_consul():
    nodes = flatten([get_consul_servers(), get_consul_clients()])
    for host in nodes:
        r = requests.get(f"https://{host}:{const.CONSUL_HTTPS_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_vault():
    vault_servers = get_vault_servers()
    for host in vault_servers:
        r = requests.get(f"https://{host}:{const.VAULT_API_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_nomad():
    nodes = flatten([get_nomad_servers(), get_nomad_clients()])
    for host in nodes:
        r = requests.get(f"https://{host}:{const.NOMAD_PORT}", verify=const.PUBLIC_CERT)
        assert r.status_code == 200


def test_vault_boostrap():
    if get_consul_servers():
        r = get_consul_health_check("vault")
        assert len(r) == len(get_vault_servers())


def test_consul_boostrap():
    r = get_consul_health_check("consul")
    assert len(r) == 0


def test_nomad_server_boostrap():
    r = get_consul_health_check("nomad")
    assert len(r) == len(get_nomad_servers() * 3)


def test_nomad_client_boostrap():
    r = get_consul_health_check("nomad-client")
    assert len(r) == len(get_nomad_clients())
