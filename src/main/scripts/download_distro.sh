#!/bin/bash

set -ueo pipefail
yum install -y wget

rm -f /workspace/distro/downloads/{*.zip,*.gz,*.war}

wget -P /workspace/distro/downloads/  https://releases.hashicorp.com/nomad/1.6.1/nomad_1.6.1_linux_amd64.zip &
wget -P /workspace/distro/downloads/  https://releases.hashicorp.com/consul/1.16.1/consul_1.16.1_linux_amd64.zip &
wget -P /workspace/distro/downloads/  https://releases.hashicorp.com/vault/1.14.1/vault_1.14.1_linux_amd64.zip &

wait

wget -P /workspace/distro/downloads/  https://dl.influxdata.com/telegraf/releases/telegraf-1.27.4_linux_amd64.tar.gz &
wget -P /workspace/distro/downloads/  https://github.com/prometheus/prometheus/releases/download/v2.44.0/prometheus-2.44.0.linux-amd64.tar.gz &
wget -P /workspace/distro/downloads/  https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.10.0-linux-x86_64.tar.gz &
wget -P /workspace/distro/downloads/  https://get.jenkins.io/war-stable/2.414.2/jenkins.war &

wait