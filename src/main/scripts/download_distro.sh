#!/bin/bash

set -ueo pipefail
yum install -y wget

NOMAD_VERSION=$(jq -r '.nomad_version' /scripts/artifacts.json)
CONSUL_VERSION=$(jq -r '.consul_version' /scripts/artifacts.json)
VAULT_VERSION=$(jq -r '.vault_version' /scripts/artifacts.json)
TELEGRAF_VERSION=$(jq -r '.telegraf_version' /scripts/artifacts.json)
PROMETHEUS_VERSION=$(jq -r '.prometheus_version' /scripts/artifacts.json)
FILEBEAT_VERSION=$(jq -r '.filebeat_version' /scripts/artifacts.json)
JENKINS_VERSION=$(jq -r '.jenkins_version' /scripts/artifacts.json)

wget -P /workspace/artifacts/downloads/  https://releases.hashicorp.com/nomad/${NOMAD_VERSION}/nomad_${NOMAD_VERSION}_linux_amd64.zip &
wget -P /workspace/artifacts/downloads/  https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip &
wget -P /workspace/artifacts/downloads/  https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip &

wait

wget -P /workspace/artifacts/downloads/  https://dl.influxdata.com/telegraf/releases/telegraf-${TELEGRAF_VERSION}_linux_amd64.tar.gz &
wget -P /workspace/artifacts/downloads/  https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-${FILEBEAT_VERSION}-linux-x86_64.tar.gz &
wget -P /workspace/artifacts/downloads/  https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz &
wget -P /workspace/artifacts/downloads/  https://get.jenkins.io/war-stable/${JENKINS_VERSION}/jenkins.war &

wait