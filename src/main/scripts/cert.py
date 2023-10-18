from utils import *
from command_helper import *


def generate_ca_private():
    command_local("openssl genrsa -out /workspace/ca-private-key.pem 4096")


def generate_ca_public(common_name):
    command_local(f"openssl req -new -x509 -sha256 -days 3560 -subj /CN={common_name} -key "
                 "/workspace/ca-private-key.pem -out /workspace/ca-public-key.pem")


def generate_agent_private():
    command_local(f"openssl genrsa -out /opt/agent/certs/agent-private-key.pem 4096")


def generate_agent_csr(common_name):
    command_local(f"openssl req -new -sha256 -subj /CN={common_name} -key /opt/agent/certs/agent-private-key.pem "
                 f"-out /opt/agent/certs/agent-csr.pem")


def generate_agent_public(san):
    with open("/tmp/extfile.conf", "w") as f:
        f.writelines(f"subjectAltName={san}")
    command_local("openssl x509 -req -sha256 -days 3560 -in /opt/agent/certs/agent-csr.pem "
                 "-CA /workspace/ca-public-key.pem -CAkey /workspace/ca-private-key.pem "
                 "-out /opt/agent/certs/agent-public-key.pem -extfile /tmp/extfile.conf -CAcreateserial 2> /dev/null")


def generate_encryption_key():
    result = command_local("openssl rand -base64 32")
    return result.stdout.decode('utf-8').strip()


def trust_ca_public():
    command_local("""
        update-ca-trust force-enable
        cp /opt/agent/certs/ca-public-key.pem /etc/pki/ca-trust/source/anchors/
        update-ca-trust extract
    """)