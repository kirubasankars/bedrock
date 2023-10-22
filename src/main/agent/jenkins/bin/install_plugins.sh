#!/bin/bash
set -ueo pipefail

function wait_for_jenkins() {
    JENKINS_URL="http://0.0.0.0:8081"
    WAIT_TIME_SECONDS=15

    while :; do
        response=$(curl --write-out '%{http_code}' --silent --output /dev/null $JENKINS_URL)

        if [ "$response" -eq 200 ]; then
            echo "Jenkins is available now."
            break
        else
            echo "Waiting for Jenkins to be available..."
            sleep $WAIT_TIME_SECONDS
        fi
    done
}

wait_for_jenkins

sleep 10 && cd /tmp && wget http://0.0.0.0:8081/jnlpJars/jenkins-cli.jar || true

for x in $(cat /opt/agent/jenkins/config/plugins.txt); do
    java -jar /tmp/jenkins-cli.jar -s http://0.0.0.0:8081/ install-plugin $x || true
done || true

wait_for_jenkins

java -jar /tmp/jenkins-cli.jar -s http://0.0.0.0:8081/ restart && sleep 10

wait_for_jenkins

