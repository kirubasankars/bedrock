import command_helper
import wait_for_machine
import os
import time

command_helper.command_remote("""
    mkdir -p /opt/agent;
    if ! test -f /opt/agent/node.txt; then        
        uuidgen > /opt/agent/host.txt
    fi
""")

command_helper.command_local("""
    useradd --shell /bin/bash -u 1050 -m agent
    mkdir -p /opt/agent
    rsync -r /agent/jenkins /opt/agent/
    bash /scripts/rsync_local_remote.sh
""")

command_helper.command_remote("""
    sh /opt/agent/jenkins/bin/infra_setup.sh
""")

try:
    command_helper.command_remote("""
        if needs-restarting -r; then
            echo "Reboot is needed. Initiating reboot..."
            sudo reboot
        else
            echo "No reboot is needed."
        fi
    """)
except:
    pass

time.sleep(10)

wait_for_machine.wait_for_machine(target_host=os.getenv("HOST"))