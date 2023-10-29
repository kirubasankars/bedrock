from cert import *
from variables import *

def main():
    generate_ca_private()
    generate_ca_public(get_cluster_id())

main()
