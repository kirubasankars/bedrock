import command_helper
import wait_for_machine
import os
import time

command_helper.command_remote("sh /opt/agent/infra/bin/setup.sh")

try:
    command_helper.command_remote("""            
        if needs-restarting -r; then 
            echo "Reboot is needed. Initiating reboot..."
            reboot now
        else
            echo "No reboot is needed."
        fi
    """)
except:
    pass

time.sleep(10)

wait_for_machine.wait_for_machine(target_host=os.getenv("HOST"))