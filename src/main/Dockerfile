FROM fedora

RUN yum update -y
RUN yum install -y python3 python3-pip jq wget rsync tree openssl openssh-clients tini docker unzip
RUN pip install requests bcrypt pytest

RUN mkdir -p /agent/{nomad,consul,vault,filebeat,telegraf,prometheus,jenkins}/{bin,data,logs,config}
RUN mkdir -p /agent/{certs,bin}

COPY agent /agent
COPY scripts /scripts
RUN chmod +x /scripts/*.sh

ENTRYPOINT ["tini", "-g", "--", "/scripts/start.sh"]