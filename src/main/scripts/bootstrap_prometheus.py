from utils import *


def bootstrap_prometheus():
    nodes = retrieve_host_ip_and_roles()
    prometheus = [ip for ip, roles in nodes.items() if "prometheus" in roles]

    if len(prometheus) > 0:
        with open("/workspace/cluster_config.env", "a") as f:
            f.write("\n")
            f.write(f"PROMETHEUS_ADDR=https://{prometheus[0]}:{const.PROMETHEUS_PORT}\n")
            f.write(f"PROMETHEUS_USER=admin\n")
            f.write(f"PROMETHEUS_PASSWORD=admin\n")


bootstrap_prometheus()
