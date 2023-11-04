# Use a base image and specify a version for reproducibility
FROM fedora:latest

# Install SSH server and other necessary packages, and ensure that the SSH host keys are generated
RUN yum -y update && \
    yum -y install openssh-server rsync && \
    yum clean all && \
    ssh-keygen -A && \
    mkdir /var/run/sshd

# Create a user and prepare .ssh directory
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Copy the public key file from the local host to the container's root .ssh directory
COPY /workspace/homelab.key.pub /root/.ssh/authorized_keys

# Correct the permissions
RUN chown root:root /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys

# Configure SSH daemon
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# Run SSH server
CMD ["/usr/sbin/sshd", "-D"]
