#!/bin/bash
set -ueo pipefail

mkdir -p /workspace/distro/{nomad,consul,vault,telegraf,prometheus,filebeat,jenkins}/{bin,config}

unzip -o -d /workspace/distro/nomad/bin/  /workspace/distro/downloads/nomad_*_linux_amd64.zip
unzip -o -d /workspace/distro/consul/bin/ /workspace/distro/downloads/consul_*_linux_amd64.zip
unzip -o -d /workspace/distro/vault/bin/  /workspace/distro/downloads/vault_*_linux_amd64.zip

tar xf /workspace/distro/downloads/telegraf-*_linux_amd64.tar.gz -C /tmp/
cp /tmp/telegraf-*/usr/bin/telegraf  /workspace/distro/telegraf/bin/

tar xf /workspace/distro/downloads/filebeat-*-linux-x86_64.tar.gz -C /tmp/
cp /tmp/filebeat-*/filebeat  /workspace/distro/filebeat/bin
cp -r /tmp/filebeat-*/module /workspace/distro/filebeat/config/
cp -r /tmp/filebeat-*/fields.yml /workspace/distro/filebeat

tar xf /workspace/distro/downloads/prometheus-*linux-amd64.tar.gz -C /tmp/
cp /tmp/prometheus-*.linux-amd64/prometheus /workspace/distro/prometheus/bin/
cp /tmp/prometheus-*.linux-amd64/promtool   /workspace/distro/prometheus/bin/
rm -fr /tmp/prometheus-*.linux-amd64

cp /workspace/distro/downloads/jenkins.war /workspace/distro/jenkins/bin/