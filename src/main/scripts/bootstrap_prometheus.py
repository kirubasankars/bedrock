from utils import *


def bootstrap_prometheus():
    prometheus = get_host_one('prometheus')

    if len(prometheus) > 0:
        with open("/workspace/cluster_config.env", "a") as f:
            f.write("\n")
            f.write(f"PROMETHEUS_ADDR=https://{prometheus[0]}:{const.PROMETHEUS_PORT}\n")
            f.write(f"PROMETHEUS_USER=admin\n")
            f.write(f"PROMETHEUS_PASSWORD=admin\n")


bootstrap_prometheus()
