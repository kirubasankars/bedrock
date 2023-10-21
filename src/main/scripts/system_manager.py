import argparse
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import command_helper
import utils

parser = argparse.ArgumentParser(description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-r", "--roles", help="filter hosts by roles", required=False, default="")
parser.add_argument("-c", "--concurrency", help="max concurrency", required=False, default=0, type=int)
parser.add_argument("-i", "--ignore_error", help="ignore_error", required=False, default=0, type=int)
parser.add_argument("-o", "--operation", help="action", required=True)
args = parser.parse_args()


def run(work_item):
    host, command_group, operation = work_item
    image = os.getenv("IMAGE_NAME")
    workspace = os.getenv("WORKSPACE")
    name = f"""{command_group}-{host.replace(".", "-")}"""
    r = command_helper.command_local(cmd=f"""
        docker run --privileged -e OPERATION="{operation}" -e HOST={host} -e NODE_OPS="1" -v {workspace}:/workspace -v /var/run/docker.sock:/var/run/docker.sock --name "{name}" {image}
    """, return_error=True)
    if r.returncode != 0:
        raise Exception(r)
    else:
        output = command_helper.command_local(cmd=f"docker logs {name}", return_error=True).stdout.decode('utf-8')
        if output:
            print(output)
        command_helper.command_local(cmd=f"""docker rm {name}""")


def main():
    command_group = uuid.uuid4()
    config = vars(args)

    ignore_error = config["ignore_error"]
    config["roles"] = [x.strip() for x in config["roles"].split(",") if x.strip()]

    nodes = utils.retrieve_host_ip_and_roles(config["roles"])
    hosts = list(nodes.keys())

    max_concurrency = config["concurrency"] or len(hosts) or 1
    work_items = list(zip(hosts, (len(hosts) * [str(command_group)]), (len(hosts) * [config["operation"]])))
    work_list = [work_items[i:i + max_concurrency] for i in range(0, len(work_items), max_concurrency)]

    if work_items:
        print(work_list, flush=True)

    for work_items in work_list:
        with ThreadPoolExecutor(max_workers=max_concurrency) as executor:
            futures = {executor.submit(run, item): item for item in work_items}
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    if ignore_error == 0:
                        sys.exit(1)


main()
