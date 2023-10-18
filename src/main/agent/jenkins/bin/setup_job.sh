#!/bin/bash
set -ueo pipefail

function wait_for_jenkins() {
    JENKINS_URL="http://0.0.0.0:8080"
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

sleep 10 && cd /tmp && wget http://0.0.0.0:8080/jnlpJars/jenkins-cli.jar || true

java -jar /tmp/jenkins-cli.jar -s http://0.0.0.0:8080/ create-job build < /opt/agent/jenkins/config/build.xml
java -jar /tmp/jenkins-cli.jar -s http://0.0.0.0:8080/ create-job release < /opt/agent/jenkins/config/release.xml