
set -ueo pipefail

CERT_ROOT=/opt/agent/certs
mkdir -p "$CERT_ROOT" || true

function generate_private_ca() {
  openssl genrsa -out "$CERT_ROOT"/ca-private-key.pem 4096
}

function generate_public_ca() {
  COMMON_NAME=$1
  openssl req -new -x509 -sha256 -days 3560 -subj "/CN=$COMMON_NAME" -key "$CERT_ROOT"/ca-private-key.pem -out "$CERT_ROOT"/ca-public-key.pem
}

function ca_info() {
  openssl x509 -in "$CERT_ROOT"/ca-public-key.pem -text
}

function cert_info() {
  openssl x509 -in "$CERT_ROOT"/agent-public-key.pem -text
}

function trust_ca_public() {
  update-ca-trust force-enable
  cp "$CERT_ROOT"/ca-public-key.pem /etc/pki/ca-trust/source/anchors/
  update-ca-trust extract
}

function generate_private_key() {
  openssl genrsa -out "$CERT_ROOT"/agent-private-key.pem 4096
}

function generate_csr() {
  COMMON_NAME=$1
  openssl req -new -sha256 -subj "/CN=$COMMON_NAME" -key "$CERT_ROOT"/agent-private-key.pem -out "$CERT_ROOT"/agent-csr.pem
}

function generate_public_key() {
  SAN=$1
  echo "subjectAltName=$SAN" >> /tmp/extfile.conf
  openssl x509 -req -sha256 -days 3560 -in "$CERT_ROOT"/agent-csr.pem -CA "$CERT_ROOT"/ca-public-key.pem -CAkey "$CERT_ROOT"/ca-private-key.pem -out "$CERT_ROOT"/agent-public-key.pem -extfile /tmp/extfile.conf -CAcreateserial
}

function generate_chain() {
    cat "$CERT_ROOT"/ca-private-key.pem "$CERT_ROOT"/agent-public-key.pem > "$CERT_ROOT"/agent-chain-key.pem
}
