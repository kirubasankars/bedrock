Bedrock is an all-encompassing infrastructure provisioning tool meticulously designed to streamline the establishment and administration of clusters containing Nomad, Consul, and Vault nodes. Each node within the cluster is equipped with Telegraf for real-time monitoring. Moreover, Prometheus monitoring nodes are set up to interact seamlessly with Telegraf, and Filebeat is meticulously configured to export logs to an OpenSearch instance. Bedrock also includes robust mechanisms for handling patching and cluster upgrades, ensuring that your environment stays current and secure. The installation process and management command-line interface (CLI) are built on top of Docker, with Docker commands invoked through a Makefile.

Here's a step-by-step guide to setting up a cluster using Bedrock:

1. Create a directory named "workspace."

2. Within the "workspace" directory, create a file named "nodes.txt" with the following format:

   ```
   192.168.1.177 nomad_server,consul_server,vault_server,nomad_client,prometheus
   ```

   In this format, each line should contain an IP address, followed by a comma-separated list of roles that define what will be configured on that machine.

3. To initiate the cluster setup process, execute the following command:

   ```
   make bootstrap
   ```

   This command triggers the Bedrock installer and management CLI to orchestrate the cluster setup. Bedrock utilizes the information in the "nodes.txt" file to deploy and configure the specified roles on each machine. This ensures the establishment of a fully functional Nomad, Consul, and Vault cluster, complete with Telegraf-based monitoring and log exporting to an OpenSearch instance via Filebeat. Additionally, Bedrock efficiently manages maintenance tasks, including patching and cluster upgrades, to ensure the ongoing security and reliability of your environment.