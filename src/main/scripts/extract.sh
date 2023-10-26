#!/bin/bash
set -ueo pipefail

NOMAD_VERSION=$(jq -r '.nomad_version' /scripts/artifacts.json)
CONSUL_VERSION=$(jq -r '.consul_version' /scripts/artifacts.json)
VAULT_VERSION=$(jq -r '.vault_version' /scripts/artifacts.json)
TELEGRAF_VERSION=$(jq -r '.telegraf_version' /scripts/artifacts.json)
PROMETHEUS_VERSION=$(jq -r '.prometheus_version' /scripts/artifacts.json)
FILEBEAT_VERSION=$(jq -r '.filebeat_version' /scripts/artifacts.json)
JENKINS_VERSION=$(jq -r '.jenkins_version' /scripts/artifacts.json)
GRAFANA_VERSION=$(jq -r '.grafana_version' /scripts/artifacts.json)

mkdir -p /workspace/artifacts/{nomad,consul,vault,telegraf,prometheus,filebeat,jenkins}/{bin,config}

mkdir -p /workspace/artifacts/nomad/bin/"${NOMAD_VERSION}"
mkdir -p /workspace/artifacts/consul/bin/"${CONSUL_VERSION}"
mkdir -p /workspace/artifacts/vault/bin/"${VAULT_VERSION}"
mkdir -p /workspace/artifacts/telegraf/bin/"${TELEGRAF_VERSION}"
mkdir -p /workspace/artifacts/filebeat/bin/"${FILEBEAT_VERSION}"
mkdir -p /workspace/artifacts/prometheus/bin/"${PROMETHEUS_VERSION}"
mkdir -p /workspace/artifacts/jenkins/bin/"${JENKINS_VERSION}"
mkdir -p /workspace/artifacts/grafana/bin/"${GRAFANA_VERSION}"

unzip -o -d /workspace/artifacts/nomad/bin/"${NOMAD_VERSION}"  /workspace/artifacts/downloads/nomad_*_linux_amd64.zip
unzip -o -d /workspace/artifacts/consul/bin/"${CONSUL_VERSION}" /workspace/artifacts/downloads/consul_*_linux_amd64.zip
unzip -o -d /workspace/artifacts/vault/bin/"${VAULT_VERSION}"  /workspace/artifacts/downloads/vault_*_linux_amd64.zip

tar xf /workspace/artifacts/downloads/telegraf-*_linux_amd64.tar.gz -C /tmp/
cp /tmp/telegraf-*/usr/bin/telegraf  /workspace/artifacts/telegraf/bin/"${TELEGRAF_VERSION}"

tar xf /workspace/artifacts/downloads/filebeat-*-linux-x86_64.tar.gz -C /tmp/
cp /tmp/filebeat-*/filebeat  /workspace/artifacts/filebeat/bin/"${FILEBEAT_VERSION}"
cp -r /tmp/filebeat-*/module /workspace/artifacts/filebeat/config/
cp -r /tmp/filebeat-*/fields.yml /workspace/artifacts/filebeat

tar xf /workspace/artifacts/downloads/grafana-*.linux-amd64.tar.gz -C /tmp/
mv /tmp/grafana-* /tmp/grafana
mv /tmp/grafana/bin/grafan* /workspace/artifacts/grafana/bin/"${GRAFANA_VERSION}"/
rsync -r /tmp/grafana /workspace/artifacts/

tar xf /workspace/artifacts/downloads/prometheus-*linux-amd64.tar.gz -C /tmp/
cp /tmp/prometheus-*.linux-amd64/prometheus /workspace/artifacts/prometheus/bin/"${PROMETHEUS_VERSION}"
cp /tmp/prometheus-*.linux-amd64/promtool   /workspace/artifacts/prometheus/bin/"${PROMETHEUS_VERSION}"

cp /workspace/artifacts/downloads/jenkins.war /workspace/artifacts/jenkins/bin/"${JENKINS_VERSION}"