import vault
import nomad
import consul

vault_token = vault.get_kv_management_token()
nomad_token = nomad.get_nomad_management_token()
consul_token = consul.get_consul_management_token()

print(f"export VAULT_TOKEN={vault_token}")
print(f"export NOMAD_TOKEN={nomad_token}")
print(f"export CONSUL_TOKEN={consul_token}")