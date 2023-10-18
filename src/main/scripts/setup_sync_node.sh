#!/bin/bash
set -ueo pipefail

if [[ -d "/opt/agent/resolved" ]]; then
  mkdir -p /etc/systemd/resolved.conf.d
  rsync /opt/agent/resolved/config/*.conf /etc/systemd/resolved.conf.d/
fi

chown root:root /opt/agent/filebeat/config/filebeat.yml
chown -R agent:agent /opt/agent

rsync /opt/agent/**/*.service /usr/lib/systemd/system/

update-ca-trust force-enable
rsync /opt/agent/certs/ca-public-key.pem /etc/pki/ca-trust/source/anchors/
update-ca-trust extract

iptables --table nat --append OUTPUT --destination localhost --protocol udp --match udp --dport 53 --jump REDIRECT --to-ports 8600
iptables --table nat --append OUTPUT --destination localhost --protocol tcp --match tcp --dport 53 --jump REDIRECT --to-ports 8600
(! grep 127.0.0.1 /etc/resolv.conf) && sed -i '1 i\nameserver      127.0.0.1' /etc/resolv.conf || true

mkdir -p /etc/docker && rsync /opt/agent/docker/config/* /etc/docker/

if ! grep "/opt/agent/profile" /etc/profile; then
  echo "source /opt/agent/profile" >> /etc/profile
fi