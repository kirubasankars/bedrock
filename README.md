# bedrock

Bedrock is a comprehensive infrastructure setup tool designed to facilitate the deployment and management of clusters consisting of Nomad, Consul, and Vault nodes. Each node in the cluster comes equipped with Telegraf for monitoring purposes, and Filebeat is configured to export logs to an OpenSearch instance. Additionally, Bedrock includes mechanisms for handling patching and upgrading of clusters. The installer and management CLI are built on top of Docker, with Docker commands invoked via a Makefile.

To set up a cluster using Bedrock, follow these steps:

1. Create a folder named "workspace."

2. Inside the "workspace" folder, create a file named "nodes.txt" with the following format:
   
   ```
   192.168.1.177 nomad_server,consul_server,vault_server,nomad_client,prometheus
   ```

   In this format, each line should contain an IP address followed by a comma-separated list of roles that define what will be configured on that machine.

3. To initiate the cluster setup, run the following command:
   
   ```
   make bootstrap
   ```

   This command will trigger the Bedrock installer and management CLI to orchestrate the cluster setup process. Bedrock will use the information in the "nodes.txt" file to deploy and configure the specified roles on each machine, ensuring a properly functioning Nomad, Consul, and Vault cluster, complete with monitoring using Telegraf and log export to OpenSearch via Filebeat. Additionally, Bedrock will handle maintenance tasks such as patching and cluster upgrades to keep your environment up to date and secure.
