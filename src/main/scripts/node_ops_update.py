import json
import sys
from pathlib import Path
from cert import *
import const


def get_host_id():
    with open("/opt/agent/node.txt", "r") as f:
        return f.read().strip()

with open("/scripts/artifacts.json", "r") as f:
    versions = json.loads(f.read())

def transpile():
    host_id = get_host_id()
    interface_name = get_network_interface_name()
    cluster_id = get_cluster_id()
    encryption_key = get_encryption_key()
    consul_token = get_consul_token()
    vault_token = get_vault_token()

    nodes = retrieve_host_ip_and_roles()
    consul_servers = [ip for ip, roles in nodes.items() if "consul_server" in roles]
    vault_servers = [ip for ip, roles in nodes.items() if "vault_server" in roles]
    nomad_servers = [ip for ip, roles in nodes.items() if "nomad_server" in roles]

    nomad_bootstrap_count = str(len(nomad_servers))
    consul_bootstrap_count = str(len(consul_servers))
    if len(consul_servers) == 1:
        consul_servers.append(consul_servers[0])
    if len(vault_servers) == 1:
        vault_servers.append(vault_servers[0])

    targets = json.dumps([f"{x}:{const.TELEGRAF_PROMETHEUS_PORT}" for x in nodes.keys()])



    for ext in ["*.json", "*.service", "*.conf", "*.yml", "*.env"]:
        for f in Path('/opt/agent/').rglob(ext):
            with open(f, 'r') as file:
                data = file.read()

            content = data.replace('$NODE_NAME', host_id)
            content = content.replace('$INTERFACE_NAME', interface_name)
            content = content.replace('$CLUSTER_ID', cluster_id)
            content = content.replace('$ENCRYPTION_KEY', encryption_key)

            if len(consul_servers) > 0:
                content = content.replace('$CONSUL_NODE1', consul_servers[0])
                content = content.replace('$CONSUL_NODE2', consul_servers[1])

            if len(vault_servers) > 0:
                content = content.replace('$VAULT_NODE1', vault_servers[0])
                content = content.replace('$VAULT_NODE2', vault_servers[1])

            content = content.replace('$CONSUL_BOOTSTRAP_COUNT', consul_bootstrap_count)
            content = content.replace('$NOMAD_BOOTSTRAP_COUNT', nomad_bootstrap_count)

            content = content.replace('$VAULT_API_PORT', const.VAULT_API_PORT)
            content = content.replace('$VAULT_CLUSTER_PORT', const.VAULT_CLUSTER_PORT)
            content = content.replace('$CONSUL_HTTP_PORT', const.CONSUL_HTTP_PORT)
            content = content.replace('$CONSUL_HTTPS_PORT', const.CONSUL_HTTPS_PORT)
            content = content.replace('$NOMAD_PORT', const.VAULT_API_PORT)
            content = content.replace('$TARGETS', targets)
            content = content.replace('$CONSUL_TOKEN', consul_token)
            content = content.replace('$VAULT_TOKEN', vault_token)

            content = content.replace('$NOMAD_VERSION', versions["nomad_version"])
            content = content.replace('$CONSUL_VERSION', versions["consul_version"])
            content = content.replace('$VAULT_VERSION', versions["vault_version"])
            content = content.replace('$TELEGRAF_VERSION', versions["telegraf_version"])
            content = content.replace('$FILEBEAT_VERSION', versions["filebeat_version"])
            content = content.replace('$PROMETHEUS_VERSION', versions["prometheus_version"])
            content = content.replace('$JENKINS_VERSION', versions["jenkins_version"])

            if content != data:
                with open(f, 'w') as file:
                    file.write(content)

def sync():
    cluster_id = get_cluster_id()
    host = os.getenv("HOST")

    command_local("""
        rsync -r /workspace/artifacts/{consul,nomad,vault,telegraf,filebeat,prometheus,jenkins}  /agent
        mkdir -p /opt/agent/certs
        bash /scripts/rsync_remote_local.sh
    """)

    if not os.path.isfile("/opt/agent/node.txt"):
        print("/opt/agent/node.txt is not found")
        sys.exit(1)

    with open(f"/opt/agent/cluster.txt", "w") as f:
        f.write(f"{cluster_id}")

    if not os.path.isfile("/opt/agent/certs/agent-private-key.pem") or os.getenv("UPDATE_CERT", "0") == "1":
        generate_agent_private()
        generate_agent_csr(cluster_id)
        generate_agent_public(f"DNS.1:localhost,DNS.2:server.{cluster_id}.consul,DNS.3:client.global.nomad,DNS.4:nomad.service.consul,DNS.5:server.global.nomad,DNS.6:vault.service.consul,IP.1:127.0.0.1,IP.2:{host}")
        command_local(f"rm /opt/agent/certs/agent-csr.pem")

    command_local(f"rsync /workspace/ca-public-key.pem /opt/agent/certs/")

    nodes = retrieve_host_ip_and_roles()
    roles = nodes.get(host, [])
    with open("/opt/agent/roles.txt", "w") as f:
        f.writelines("\n".join(roles))

    command_local("""
        touch /opt/agent/profile        
        rsync -r /agent/bin /opt/agent/
        rsync -r /agent/certs /opt/agent/
        rsync -r /agent/telegraf /opt/agent/
        rsync -r /agent/filebeat /opt/agent/
        rsync -r /agent/docker /opt/agent/        
        rm -f /workspace/ca-public-key.srl | true
    """)

    if "vault_server" in roles:
        command_local("rsync -r /agent/vault /opt/agent/")

    if "consul_server" in roles:
        command_local("rsync -r --exclude='consul-client*' /agent/consul /opt/agent/")
        command_local("rsync -r /agent/resolved /opt/agent/")

    if "consul_client" in roles:
        command_local("rsync -r --exclude='consul-server*' /agent/consul /opt/agent/")
        command_local("rsync -r /agent/resolved /opt/agent/")

    if "nomad_server" in roles:
        command_local("rsync -r --exclude='nomad-client*' /agent/nomad /opt/agent/")
        command_local("mv /opt/agent/nomad/config/nomad-server.env /opt/agent/nomad/config/nomad.env")

    if "nomad_client" in roles:
        nomad_roles = roles.copy()
        nomad_roles.remove("telegraf")
        nomad_roles.remove("filebeat")
        command_local("rsync -r --exclude='nomad-server*' /agent/nomad /opt/agent/")
        with open("/opt/agent/nomad/config/nomad-meta.json", "w") as f:
            f.write(json.dumps({"client": {"meta": [{x : "true" for x in list(set(nomad_roles))}]}}, indent=4))

    if "prometheus" in roles:
        command_local("rsync -r /agent/prometheus /opt/agent/")

    if "jenkins" in roles:
        command_local("rsync -r /agent/jenkins /opt/agent/")

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

    command_local("""        
        bash /scripts/rsync_local_remote.sh        
    """)

    r = command_file_remote("/scripts/setup_sync_node.sh")
    if r.returncode != 0:
        print(r.stderr.decode('utf-8'))
        sys.exit(r.returncode)

sync()