import json
import os
import sys
from pathlib import Path

import cert
import command_helper
import const
import utils
import variables
import vault


def get_host_id():
    with open("/opt/agent/node.txt", "r") as f:
        return f.read().strip()


with open("/scripts/artifacts.json", "r") as f:
    versions = json.loads(f.read())


def transpile():
    host_id = get_host_id()

    interface_name = variables.get_network_interface_name()
    cluster_id = variables.get_cluster_id()

    encryption_key = vault.get_kv_cluster_config("encryption_key") or ""
    nomad_integration_vault_token = vault.get_kv_cluster_config("nomad_integration_vault_token") or variables.get_vault_token()
    prometheus_metrics_vault_token = vault.get_kv_cluster_config("prometheus_metrics_vault_token") or ""
    nomad_integration_consul_token = vault.get_kv_cluster_config("nomad_integration_consul_token") or ""

    nodes = utils.retrieve_host_and_roles()

    consul_servers = utils.get_host_list('consul_server')
    consul_clients = utils.get_host_list('consul_client')
    nomad_servers = utils.get_host_list('nomad_server')
    nomad_clients = utils.get_host_list('nomad_client')
    vault_servers = utils.get_host_list('vault_server')

    nomad_bootstrap_count = str(len(nomad_servers))
    consul_bootstrap_count = str(len(consul_servers))
    if len(consul_servers) == 1:
        consul_servers.append(consul_servers[0])
    if len(vault_servers) == 1:
        vault_servers.append(vault_servers[0])

    consul_clients_only = list(set(consul_clients).difference(consul_servers))
    nomad_clients_only = list(set(nomad_clients).difference(nomad_servers))

    values = {
        "$NODE_NAME": host_id,
        "$INTERFACE_NAME": interface_name,
        "$CLUSTER_ID": cluster_id,
        "$ENCRYPTION_KEY": encryption_key,
        "$CONSUL_BOOTSTRAP_COUNT": consul_bootstrap_count,
        "$NOMAD_BOOTSTRAP_COUNT": nomad_bootstrap_count,
        "$VAULT_API_PORT": const.VAULT_API_PORT,
        "$VAULT_CLUSTER_PORT": const.VAULT_CLUSTER_PORT,
        "$CONSUL_HTTP_PORT": const.CONSUL_HTTP_PORT,
        "$CONSUL_HTTPS_PORT": const.CONSUL_HTTPS_PORT,
        "$NOMAD_PORT": const.VAULT_API_PORT,
        "$NOMAD_INTEGRATION_CONSUL_TOKEN": nomad_integration_consul_token,
        "$NOMAD_INTEGRATION_VAULT_TOKEN": nomad_integration_vault_token,
        "$PROMETHEUS_METRICS_VAULT_TOKEN": prometheus_metrics_vault_token,
        "$NOMAD_VERSION": versions["nomad_version"],
        "$CONSUL_VERSION": versions["consul_version"],
        "$VAULT_VERSION": versions["vault_version"],
        "$TELEGRAF_VERSION": versions["telegraf_version"],
        "$FILEBEAT_VERSION": versions["filebeat_version"],
        "$PROMETHEUS_VERSION": versions["prometheus_version"],
        "$JENKINS_VERSION": versions["jenkins_version"],
        "$GRAFANA_VERSION": versions["grafana_version"],
        "$ALL_TARGETS": json.dumps([f"{x}:{const.TELEGRAF_PROMETHEUS_PORT}" for x in nodes.keys()]),
        "$CONSUL_SERVER_TARGETS": json.dumps([f"{x}:{const.CONSUL_HTTPS_PORT}" for x in set(consul_servers)]),
        "$CONSUL_CLIENT_TARGETS": json.dumps([f"{x}:{const.CONSUL_HTTPS_PORT}" for x in consul_clients_only]),
        "$NOMAD_SERVER_TARGETS": json.dumps([f"{x}:{const.NOMAD_PORT}" for x in set(nomad_servers)]),
        "$NOMAD_CLIENT_TARGETS": json.dumps([f"{x}:{const.NOMAD_PORT}" for x in nomad_clients_only]),
        "$VAULT_SERVER_TARGETS": json.dumps([f"{x}:{const.VAULT_API_PORT}" for x in set(vault_servers)])
    }

    for ext in ["*.json", "*.service", "*.conf", "*.yml", "*.env", "*.token"]:
        for f in Path('/opt/agent/').rglob(ext):
            with open(f, 'r') as file:
                data = file.read()

            content = data

            for k, v in values.items():
                content = content.replace(k, v)

            if len(consul_servers) > 0:
                content = content.replace('$CONSUL_NODE1', consul_servers[0])
                content = content.replace('$CONSUL_NODE2', consul_servers[1])

            if len(vault_servers) > 0:
                content = content.replace('$VAULT_NODE1', vault_servers[0])
                content = content.replace('$VAULT_NODE2', vault_servers[1])

            if content != data:
                with open(f, 'w') as file:
                    file.write(content)


def sync():
    cluster_id = variables.get_cluster_id()
    host = os.getenv("HOST")

    if not os.path.isfile("/workspace/ca.key"):
        cert.generate_ca_private()
        cert.generate_ca_public(variables.get_cluster_id())

    command_helper.command_local("""
        rsync -r /workspace/artifacts/{consul,nomad,vault,telegraf,filebeat,prometheus,jenkins}  /agent
        mkdir -p /opt/agent/certs
        bash /scripts/rsync_remote_local.sh
    """)

    if not os.path.isfile("/opt/agent/node.txt"):
        print("/opt/agent/node.txt is not found")
        sys.exit(1)

    with open(f"/opt/agent/cluster.txt", "w") as f:
        f.write(f"{cluster_id}")

    if not os.path.isfile("/opt/agent/certs/agent.key") or os.getenv("UPDATE_CERT", "0") == "1":
        cert.generate_site_private("agent")
        cert.generate_site_csr("agent", cluster_id)
        cert.generate_site_public("agent",
                                  f"DNS.1:localhost,DNS.2:server.{cluster_id}.consul,DNS.3:client.global.nomad,DNS.4:nomad.service.consul,DNS.5:server.global.nomad,DNS.6:vault.service.consul,IP.1:127.0.0.1,IP.2:{host}")
        command_helper.command_local(f"rm /opt/agent/certs/agent.csr")

    command_helper.command_local(f"rsync /workspace/ca.crt /opt/agent/certs/")

    nodes = utils.retrieve_host_and_roles()
    roles = nodes.get(host, [])
    with open("/opt/agent/roles.txt", "w") as f:
        f.writelines("\n".join(roles))

    command_helper.command_local("""
        touch /opt/agent/profile        
        rsync -r /agent/bin /opt/agent/
        rsync -r /agent/certs /opt/agent/
        rsync -r /agent/telegraf /opt/agent/
        rsync -r /agent/filebeat /opt/agent/
        rsync -r /agent/docker /opt/agent/        
        rm -f /workspace/ca-public-key.srl | true
    """)

    if "vault_server" in roles:
        command_helper.command_local("rsync -r /agent/vault /opt/agent/")

    if "consul_server" in roles:
        command_helper.command_local("rsync -r --exclude='consul-client*' /agent/consul /opt/agent/")
        command_helper.command_local("rsync -r /agent/resolved /opt/agent/")

    if "consul_client" in roles:
        command_helper.command_local("rsync -r --exclude='consul-server*' /agent/consul /opt/agent/")
        command_helper.command_local("rsync -r /agent/resolved /opt/agent/")

    if "nomad_server" in roles:
        command_helper.command_local("rsync -r --exclude='nomad-client*' /agent/nomad /opt/agent/")
        command_helper.command_local("mv /opt/agent/nomad/config/nomad-server.env /opt/agent/nomad/config/nomad.env")

    if "nomad_client" in roles:
        nomad_roles = roles.copy()
        nomad_roles.remove("telegraf")
        nomad_roles.remove("filebeat")
        command_helper.command_local("rsync -r --exclude='nomad-server*' /agent/nomad /opt/agent/")
        with open("/opt/agent/nomad/config/nomad-meta.json", "w") as f:
            f.write(json.dumps({"client": {"meta": [{x: "true" for x in list(set(nomad_roles))}]}}, indent=4))

    if "prometheus" in roles:
        command_helper.command_local("rsync -r /agent/prometheus /opt/agent/")

    if "grafana" in roles:
        command_helper.command_local("rsync -r /agent/grafana /opt/agent/")

    if "jenkins" in roles:
        command_helper.command_local("rsync -r /agent/jenkins /opt/agent/")

    transpile()

    if len([x for x in roles if "consul" in x]) > 0:
        with open("/opt/agent/profile", "a") as f:
            f.writelines(f"alias consul=/opt/agent/consul/bin/{versions['consul_version']}/consul\n")
            f.writelines("export CONSUL_HTTP_SSL=true\n")
            f.writelines(f"export CONSUL_HTTP_ADDR={host}:{const.CONSUL_HTTPS_PORT}\n")

    if len([x for x in roles if "nomad" in x]) > 0:
        with open("/opt/agent/profile", "a") as f:
            f.writelines(f"alias nomad=/opt/agent/nomad/bin/{versions['nomad_version']}/nomad\n")
            f.writelines(f"export NOMAD_ADDR=https://{host}:{const.NOMAD_PORT}\n")

    if len([x for x in roles if "vault" in x]) > 0:
        with open("/opt/agent/profile", "a") as f:
            f.writelines(f"alias vault=/opt/agent/vault/bin/{versions['vault_version']}/vault\n")
            f.writelines(f"export VAULT_ADDR=https://{host}:{const.VAULT_API_PORT}\n")

    command_helper.command_local("""        
        bash /scripts/rsync_local_remote.sh        
    """)

    r = command_helper.command_file_remote("/scripts/setup_sync_node.sh")
    if r.returncode != 0:
        print(r.stderr.decode('utf-8'))
        sys.exit(r.returncode)


sync()
