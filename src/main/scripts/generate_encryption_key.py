import cert
import vault

vault.put_kv_cluster_config("encryption_key", {"key": cert.generate_encryption_key()})