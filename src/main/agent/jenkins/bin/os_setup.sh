#!/bin/bash
set -ueo pipefail

yum update -y && yum install -y java-17-openjdk docker make git wget python

/usr/bin/systemctl daemon-reload
/usr/bin/systemctl enable --now docker

username=agent
if ! id "$username" &>/dev/null; then
   groupadd --gid 1051 $username || true
   useradd --shell /bin/bash -g $username -u 1052 $username || true
fi
usermod -aG docker agent || true

mkdir -p /opt/agent

uuidgen > /opt/agent/node.txt