import os
import sys
import time

import command_helper
import wait_for_machine

command_helper.command_remote("""
    mkdir -p /opt/agent/certs;
    if ! test -f /opt/agent/node.txt; then        
        uuidgen > /opt/agent/node.txt
    fi
""")

command_helper.command_local("""
    mkdir -p /opt/agent/certs;
    rsync -r /agent/jenkins /opt/agent/
    bash /scripts/rsync_local_remote.sh
""")

command_helper.command_remote("""
    sh /opt/agent/jenkins/bin/os_setup.sh
""")

try:
    command_helper.command_remote("""
        if ! needs-restarting -r >/dev/null; then
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
