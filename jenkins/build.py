import random
import subprocess
import sys

def get_hosts():
    hosts = []
    with open("./workspace/hosts.txt", "r") as f:
        lines = [x for x in f.read().split("\n")  if len(x.strip()) > 0]
        for line in lines:
            if "jenkins" in line:
                continue
            hosts.append(line.split(" ")[0].strip())
    return hosts

def get_clusters():
    return [
        [
            [
                ["vault_server", "nomad_server", "consul_server", "prometheus"]
            ],
            [
                ["vault_server", "nomad_server", "consul_server", "prometheus"],
                ["nomad_client"]
            ]
        ],

        [
            [
                ["vault_server"],
                ["nomad_server", "consul_server", "nomad_client"]
            ],
            [
                ["vault_server"],
                ["nomad_server", "consul_server", "nomad_client"],
                ["prometheus"]
            ]
        ],

        [
            [
                ["consul_server"],
                ["nomad_server", "vault_server"]
            ],
            [
                ["consul_server", "prometheus"],
                ["nomad_server", "vault_server"],
                ["nomad_client"]
            ],
            [
                ["consul_server", "prometheus"],
                ["nomad_server", "vault_server"],
                ["nomad_client"],
                ["nomad_client"]
            ]
        ],

        [
            [
                ["consul_server", "prometheus"],
                ["vault_server", "nomad_client"],
                ["nomad_server"]
            ],
            [
                ["consul_server", "vault_server", "nomad_server", "nomad_client", "prometheus"],
                ["consul_server", "vault_server", "nomad_server", "nomad_client"],
                ["consul_server", "vault_server", "nomad_server", "nomad_client"]
            ],
        ],

        [
            [
                ["consul_server", "vault_server", "nomad_server", "nomad_client"],
                ["consul_server", "vault_server", "nomad_server"],
                ["consul_server", "vault_server", "nomad_server"],
                ["nomad_client", "prometheus"]
            ]
        ]
    ]

hosts = get_hosts()
clusters = get_clusters()
random.seed(1)

with open(f"./workspace/hosts.txt", "r") as f:
    nodes_txt = f.read()

for cluster in clusters:
    with open(f"./workspace/hosts.txt", "w") as f:
        f.write(nodes_txt)

    r = subprocess.run(["make", "cleanup"])

    print("-----")
    cluster_nodes = []
    for index, step in enumerate(cluster):
        available_hosts = list(set(cluster_nodes) ^ (set(hosts)))
        if len(available_hosts) >= (len(step) - len(cluster_nodes)):
            selected_hosts = random.sample(population=available_hosts, k=len(step) - len(cluster_nodes))
            cluster_nodes.extend(selected_hosts)
            nodes = []
            for x in range(len(cluster_nodes)):
                host = cluster_nodes[x]
                roles = step[x]
                nodes.append(f"{host} {','.join(roles)}")

            print(nodes)

            with open(f"./workspace/hosts.txt", "w") as f:
                f.write("\n".join(nodes))

            if index == 0:
                r = subprocess.run(["make", "cleanup", "bootstrap", "restart", "down", "up"])
            else:
                r = subprocess.run(["make", "update", "restart", "down", "up"])

            if r.returncode != 0:
                sys.exit(r.returncode)