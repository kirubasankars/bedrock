from command_helper import *


def main():
    command_remote("""
        for x in consul nomad vault telegraf prometheus jenkins grafana; do
          if test -f /usr/lib/systemd/system/$x.service; then
            /usr/bin/systemctl disable $x || true
            /usr/bin/systemctl stop $x    || true
            rm -r /usr/lib/systemd/system/$x.service || true
          fi
        done
        
        if [ "$(docker ps -a -q | wc -l)" -gt "0" ]; then
            docker stop $(docker ps -a -q)
        fi

        if [ "$(docker volume ls -q | wc -l)" -gt "0" ]; then
            docker volume rm $(docker volume ls -q) || true
        fi

        docker system prune -af || true        
        for x in $(mount | grep alloc | awk '{ print $3 }'); do umount $x || true; done

        [ -d /opt/agent ] && rm -r /opt/agent || true
        sed -i '/source \/opt\/agent\/profile/d' /etc/profile                                
    """)


main()
