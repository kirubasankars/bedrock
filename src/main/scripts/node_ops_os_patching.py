import os
import time

import command_helper
import wait_for_machine

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

# TODO: wait for consul to be green