import os
import time
import uuid

import command_helper
import wait_for_machine

command_helper.command_remote("""
    mkdir -p /opt/agent/certs
""")

command_helper.command_local("""
    mkdir -p /opt/agent/certs        
    bash /scripts/rsync_remote_local.sh    
""")

file_path = "/opt/agent/node.txt"

if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write(str(uuid.uuid4()))

    command_helper.command_local("""
        rsync -r /agent/bin /opt/agent/
        bash /scripts/rsync_local_remote.sh              
    """)

    command_helper.command_remote("sh /opt/agent/bin/os_setup.sh")

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
