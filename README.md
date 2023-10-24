Bedrock emerges as a sophisticated and holistic solution designed for infrastructure provisioning, adeptly supporting the seamless creation and management of clusters integrated with Nomad, Consul, and Vault nodes. Each node within this robust cluster is meticulously equipped with Telegraf, ensuring real-time monitoring capabilities are at your fingertips. Furthermore, the integration of Prometheus monitoring nodes with Telegraf is streamlined, while Filebeat is expertly configured to relay logs to an OpenSearch instance. Bedrock stands out with its advanced functionalities for managing software updates and cluster upgrades, ensuring your system remains secure and up-to-date. Both the setup process and the management command-line interface (CLI) are ingeniously built on Docker, employing Docker commands executed via a Makefile.

Embark on this comprehensive guide to configure your cluster using Bedrock:

1. Clone the repository from https://github.com/kirubasankars/bedrock 

2. Inside the cloned directory, create a new folder named "workspace."

3. Within the "workspace" folder, generate a file named "hosts.txt" and format it as follows:

   ```
   192.168.1.177 nomad_server,consul_server,vault_server,nomad_client,prometheus
   ```
   Please note that for roles like consul_server, nomad_server, and vault_server, you should have either 1 or 3 instances for optimal performance and redundancy. There are no specific rules for other roles; you can assign them as per your requirements. Each line in the "hosts.txt" file should contain an IP address, followed by a comma-separated list of roles. These roles are crucial as they determine the specific configurations that will be applied to each machine.

4. Transfer your SSH keys to the workspace folder, ensuring that the host machines are accessible via this key.

5. Create a file named "variables.env" and populate it with the following content:

   ```
   CLUSTER_ID=clustername # Define the cluster name
   NETWORK_INTERFACE_NAME="enp0s3" # Specify the network interface for hosting services
   SSH_USER="root" # Set the SSH user
   SSH_KEY=homelab.key  # Indicate the SSH key name for login
   ```

6. Download the required binary artifacts using the following command, and make sure to place Nomad, Consul, Vault, Jenkins, and other necessary binary files inside the "artifacts" folder within "workspace":

   ```
   make download_artifacts
   ```

7. Initiate the cluster configuration by running:

   ```
   make bootstrap
   ```

   Executing this command activates the Bedrock installer and management CLI, prompting the configuration of your cluster. Relying on the data provided in the "hosts.txt" file, Bedrock deploys and configures the specified roles on each machine, culminating in a fully functional cluster with Nomad, Consul, Vault, and augmented with Telegraf and Filebeat for comprehensive monitoring and log management. Bedrock not only excels in initial setup but also in conducting routine maintenance tasks such as patching and upgrades, bolstering the security and performance of your infrastructure.