#!/bin/bash
mkdir -p /opt/agent/certs
rsync -rahzv --rsh="ssh -o StrictHostKeyChecking=no -o LogLevel=error -l $SSH_USER" --include='*.txt' --exclude='*' $HOST:/opt/agent/ /opt/agent/
rsync -rahzv --rsh="ssh -o StrictHostKeyChecking=no -o LogLevel=error -l $SSH_USER" --include='*.pem' --exclude='*' $HOST:/opt/agent/certs/ /opt/agent/certs/