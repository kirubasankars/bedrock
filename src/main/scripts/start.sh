#!/bin/bash
set -ueo pipefail

touch /workspace/variables.env
source /workspace/variables.env

export CLUSTER_ID=${CLUSTER_ID:-"undefined"}
export NETWORK_INTERFACE_NAME=${NETWORK_INTERFACE_NAME:-"eth0"}
export UPDATE_CERT=${UPDATE_CERT:="0"}
export SSH_USER=${SSH_USER:-""}
export SSH_KEY=${SSH_KEY:-""}
export IMAGE_NAME=$(docker inspect --format='{{.Config.Image}}' "$HOSTNAME")
export NODE_OPS=${NODE_OPS:-"0"}
export MAX_CONCURRENCY=${MAX_CONCURRENCY:-"4"}

# shellcheck disable=SC2046
eval $(ssh-agent -s) > /dev/null
ssh-add /workspace/"${SSH_KEY}" 2> /dev/null
echo "StrictHostKeyChecking accept-new" >> /etc/ssh/ssh_config

touch /workspace/vault_token.txt
export VAULT_TOKEN=$(cat /workspace/vault_token.txt)

if [ "$NODE_OPS" == "1" ]; then
  python3 /scripts/"node_ops_$OPERATION".py
  exit 0
fi

if [ "$OPERATION" == "download_artifacts" ]; then
  rm -fr /workspace/downloads
  mkdir -p /workspace/downloads
  bash /scripts/download_artifacts.sh
  bash /scripts/extract.sh
elif [ "$OPERATION" == "cleanup" ]; then
  rm -f /workspace/{ca.crt,ca.key,ca.srl,vault_token.txt,vault_unseal_tokens.txt}
  python3 /scripts/system_manager.py --operation cleanup
elif [ "$OPERATION" == "validate" ]; then
  pytest -s /scripts/test_up.py
elif [ "$OPERATION" == "bootstrap" ]; then
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation os_setup
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation update
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation telegraf_up
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation filebeat_up
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles consul_server --operation consul_up && sleep 15
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles consul_client --operation consul_up
  python3 /scripts/wait_for_consul.py
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles vault_server --operation vault_up
  python3 /scripts/wait_for_vault_sealed.py
  python3 /scripts/bootstrap_vault.py
  export VAULT_TOKEN=$(cat /workspace/vault_token.txt)
  python3 /scripts/unseal_vault.py
  python3 /scripts/wait_for_vault.py
  python3 /scripts/bootstrap2_vault.py
  python3 /scripts/bootstrap_consul.py
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation update
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles nomad_server --operation nomad_up && sleep 15
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles nomad_client --operation nomad_up
  python3 /scripts/wait_for_nomad_server.py
  python3 /scripts/wait_for_nomad_client.py
  python3 /scripts/bootstrap_nomad.py
  python3 /scripts/update_policies.py
  python3 /scripts/update_integration_tokens.py
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation update
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles nomad_server --operation nomad_restart && sleep 15
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles nomad_client --operation nomad_restart
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles prometheus --operation prometheus_up
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles grafana --operation grafana_up
  pytest -s /scripts/test_up.py
  rm -f /workspace/ca.srl
elif [ "$OPERATION" == "update" ]; then
  # TODO: update certs if expired, this helps to bring back cluster which stopped for long time.
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles consul_server --operation consul_up && sleep 15
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles consul_client --operation consul_up
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --roles vault_server --operation vault_up
  python3 /scripts/wait_for_vault_sealed.py
  python3 /scripts/unseal_vault.py
  python3 /scripts/wait_for_vault.py
  python3 /scripts/update_policies.py
  python3 /scripts/update_integration_tokens.py
  python3 /scripts/system_manager.py --operation os_setup
  python3 /scripts/system_manager.py --concurrency "$MAX_CONCURRENCY" --operation update
elif [ "$OPERATION" == "os_patching" ]; then
  python3 /scripts/system_manager.py --concurrency 1 --operation os_patching
elif [ "$OPERATION" == "restart" ]; then
  python3 /scripts/system_manager.py --roles telegraf --operation telegraf_restart
  python3 /scripts/system_manager.py --roles filebeat --operation filebeat_restart
  python3 /scripts/system_manager.py --roles prometheus --operation prometheus_restart
  python3 /scripts/system_manager.py --roles grafana --operation grafana_restart
  python3 /scripts/system_manager.py --concurrency 1 --roles consul_server --operation consul_restart
  python3 /scripts/system_manager.py --roles consul_client --operation consul_restart
  python3 /scripts/system_manager.py --concurrency 1 --roles vault_server --operation vault_restart
  python3 /scripts/system_manager.py --concurrency 1 --roles nomad_server --operation nomad_restart
  python3 /scripts/system_manager.py --roles nomad_client --operation nomad_restart
  python3 /scripts/wait_for_nomad_client.py
  pytest -s /scripts/test_up.py
elif [ "$OPERATION" == "up" ]; then
  python3 /scripts/system_manager.py --roles telegraf --operation telegraf_up
  python3 /scripts/system_manager.py --roles filebeat --operation filebeat_up
  python3 /scripts/system_manager.py --roles prometheus --operation prometheus_up
  python3 /scripts/system_manager.py --roles grafana --operation grafana_up
  python3 /scripts/system_manager.py --roles consul_server --operation consul_up && sleep 15
  python3 /scripts/system_manager.py --roles consul_client --operation consul_up
  python3 /scripts/wait_for_consul.py
  python3 /scripts/system_manager.py --roles vault_server --operation vault_up
  python3 /scripts/system_manager.py --roles nomad_server --operation nomad_up && sleep 15
  python3 /scripts/system_manager.py --roles nomad_client --operation nomad_up
  python3 /scripts/wait_for_vault_sealed.py
  python3 /scripts/unseal_vault.py
  python3 /scripts/wait_for_vault.py
  python3 /scripts/wait_for_nomad_server.py
  python3 /scripts/wait_for_nomad_client.py
  pytest -s /scripts/test_up.py
elif [ "$OPERATION" == "down" ]; then
  python3 /scripts/system_manager.py --roles prometheus --operation prometheus_down
  python3 /scripts/system_manager.py --roles grafana --operation grafana_down
  python3 /scripts/system_manager.py --roles nomad_server --operation nomad_down
  python3 /scripts/system_manager.py --roles nomad_client --operation nomad_down
  python3 /scripts/system_manager.py --roles vault_server --operation vault_down
  python3 /scripts/system_manager.py --roles consul_client --operation consul_down
  python3 /scripts/system_manager.py --roles consul_server --operation consul_down
  python3 /scripts/system_manager.py --roles filebeat --operation filebeat_down
  python3 /scripts/system_manager.py --roles telegraf --operation telegraf_down
elif [ "$OPERATION" == "run_command" ]; then
  roles=${ROLES:-""}
  max_concurrency=${MAX_CONCURRENCY:-0}
  ignore_error=${IGNORE_ERROR:-0}
  touch /workspace/command.sh && python3 /scripts/system_manager.py --roles "$roles" --concurrency "$max_concurrency" --ignore_error "$ignore_error" --operation run_command
elif [ "$OPERATION" == "unseal" ]; then
  python3 /scripts/wait_for_vault_sealed.py
  python3 /scripts/unseal_vault.py
  python3 /scripts/wait_for_vault.py
  pytest -s /scripts/test_up.py
elif [ "$OPERATION" == "jenkins" ]; then
  python3 /scripts/system_manager.py --roles jenkins --operation jenkins_os_setup
  python3 /scripts/system_manager.py --roles jenkins --operation update
  python3 /scripts/system_manager.py --roles jenkins --operation jenkins_up && sleep 10
  python3 /scripts/system_manager.py --roles jenkins --operation jenkins_import_jobs
fi