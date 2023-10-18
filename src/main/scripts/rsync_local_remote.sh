#!/bin/bash
rsync -rahzv --rsh="ssh -o StrictHostKeyChecking=no -o LogLevel=error -l $SSH_USER" /opt/agent/ $HOST:/opt/agent/