import command_helper

command_helper.command_remote("""
    mkdir -p /build.git && cd /build.git && [[ ! -d "./.git" ]] && git init --bare || true
    sh /opt/agent/jenkins/bin/setup_job.sh    
""")
