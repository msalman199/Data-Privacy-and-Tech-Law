<div align="center">

# 🔐 Encrypting Personal Data at Rest with LUKS and KMS

![LUKS](https://img.shields.io/badge/LUKS-Disk%20Encryption-2C3E50?style=for-the-badge&logo=linux&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Vault](https://img.shields.io/badge/HashiCorp%20Vault-000000?style=for-the-badge&logo=vault&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-003399?style=for-the-badge&logo=europeanunion&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

*A layered data-at-rest protection lab: disk encryption, field-level encryption, and key lifecycle management*

</div>

---

## 📖 Table of Contents

- [🎯 Objectives](#-objectives)
- [📋 Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [💽 Task 1: Provision an Encrypted LUKS Volume](#-task-1-provision-an-encrypted-luks-volume)
- [🐘 Task 2: Configure PostgreSQL with pgcrypto](#-task-2-configure-postgresql-with-pgcrypto)
- [🗝️ Task 3: Manage Keys with HashiCorp Vault (Local Dev Mode)](#️-task-3-manage-keys-with-hashicorp-vault-local-dev-mode)
- [🔄 Task 4: Rotate Keys and Verify Ciphertext Changes](#-task-4-rotate-keys-and-verify-ciphertext-changes)
- [📋 Task 5: Map Controls to PDPL/GDPR Articles](#-task-5-map-controls-to-pdplgdpr-articles)
- [✅ Verification](#-verification)
- [🔧 Troubleshooting](#-troubleshooting)
- [🎯 MITRE ATT&CK Mapping](#-mitre-attck-mapping)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Objectives

| # | By the end of this lab, you will be able to... |
|---|---|
| 1 | Create and mount an encrypted LUKS volume for database storage |
| 2 | Implement column-level encryption in PostgreSQL using pgcrypto |
| 3 | Deploy HashiCorp Vault locally to manage encryption keys |
| 4 | Rotate encryption keys and verify ciphertext changes |
| 5 | Map cryptographic controls to GDPR Article 32 and GCC PDPL requirements |

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| Linux command line | Familiarity — file permissions, package managers |
| SQL / relational databases | Basic understanding |
| Encryption concepts | Conceptual knowledge of symmetric encryption and key management |
| GDPR knowledge | Understanding of Article 32 (security of processing) is helpful |

## 🖥️ Lab Environment

> A single Linux machine (Ubuntu 22.04 or similar) is provisioned via **Start Lab**. Root or sudo access and internet access to install packages are required.

```bash
# 📦 Install required packages
sudo apt update
sudo apt install -y cryptsetup postgresql postgresql-contrib \
    unzip wget gnupg jq
```

```bash
# 🗝️ Install HashiCorp Vault (open-source binary)
wget https://releases.hashicorp.com/vault/1.17.2/vault_1.17.2_linux_amd64.zip
unzip vault_1.17.2_linux_amd64.zip
sudo mv vault /usr/local/bin/
vault --version
```

---

## 💽 Task 1: Provision an Encrypted LUKS Volume

```bash
# 📀 Create a virtual disk file to act as your encrypted block device
sudo fallocate -l 1G /var/lib/db_disk.img
sudo losetup -fP /var/lib/db_disk.img
losetup -a   # note the assigned loop device, e.g. /dev/loop0
```

Initialize LUKS encryption on the loop device:

```bash
# TODO: Run cryptsetup luksFormat on your loop device
# Reference: cryptsetup luksFormat <device>
# You will be prompted to confirm and set a passphrase
```

Open the encrypted volume and create a filesystem:

```bash
sudo cryptsetup luksOpen /dev/loopX secure_pgdata
sudo mkfs.ext4 /dev/mapper/secure_pgdata
```

Mount it to a directory that PostgreSQL will use:

```bash
sudo mkdir -p /mnt/secure_pgdata
sudo mount /dev/mapper/secure_pgdata /mnt/secure_pgdata
sudo chown postgres:postgres /mnt/secure_pgdata
```

> ✅ **Checkpoint:** Run `lsblk` — confirm your loop device shows as `crypt` type, mounted at `/mnt/secure_pgdata`.

---

## 🐘 Task 2: Configure PostgreSQL with pgcrypto

Point PostgreSQL's data storage toward the encrypted mount (for this lab, create a tablespace instead of moving the full data directory):

```bash
sudo -u postgres psql -c "CREATE TABLESPACE secure_ts LOCATION '/mnt/secure_pgdata';"
```

Create a database and table using the encrypted tablespace:

```sql
-- Run inside psql
CREATE DATABASE privacy_db TABLESPACE secure_ts;
\c privacy_db
CREATE EXTENSION pgcrypto;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name TEXT,
    national_id_encrypted BYTEA
);
```

Insert encrypted PII using pgcrypto's symmetric encryption functions:

```sql
-- TODO: Use pgp_sym_encrypt() to insert an encrypted national ID
-- Example function signature:
-- pgp_sym_encrypt(data TEXT, psw TEXT) RETURNS BYTEA
INSERT INTO customers (full_name, national_id_encrypted)
VALUES ('Ahmed Al-Farsi', pgp_sym_encrypt('784-1990-1234567', 'REPLACE_WITH_KEY'));
```

Query and decrypt to verify:

```sql
-- TODO: Use pgp_sym_decrypt() to read the value back
SELECT full_name, pgp_sym_decrypt(national_id_encrypted, 'REPLACE_WITH_KEY')
FROM customers;
```

> ✅ **Checkpoint:** Confirm `national_id_encrypted` is unreadable binary in raw form but decrypts correctly with the correct key.

---

## 🗝️ Task 3: Manage Keys with HashiCorp Vault (Local Dev Mode)

```bash
# 🚀 Start Vault in dev mode (single node, in-memory, for lab purposes only)
vault server -dev -dev-listen-address="0.0.0.0:8200" &
export VAULT_ADDR="http://127.0.0.1:8200"
```

Copy the Root Token printed in the terminal output, then authenticate:

```bash
export VAULT_TOKEN="<paste_root_token_here>"
vault status
```

Enable the KV secrets engine and store your pgcrypto key:

```bash
vault secrets enable -path=secret kv-v2

# TODO: Write a secret named "pii-key" with a key-value pair
# Reference: vault kv put secret/pii-key value="<your-key>"
```

Retrieve the key programmatically instead of hardcoding it:

```bash
vault kv get -field=value secret/pii-key
```

Update your PostgreSQL insert/select statements to pull the key dynamically:

```bash
# TODO: Write a shell snippet that:
# 1. Fetches the key from Vault into a variable
# 2. Passes it into a psql command using -v or environment substitution
KEY=$(vault kv get -field=value secret/pii-key)
psql -d privacy_db -c "SELECT pgp_sym_decrypt(national_id_encrypted, '${KEY}') FROM customers;"
```

> ✅ **Checkpoint:** Confirm decryption succeeds only when the correct key is fetched from Vault.

---

## 🔄 Task 4: Rotate Keys and Verify Ciphertext Changes

```bash
# 🔄 Generate a new key value and store it as a new Vault version
vault kv put secret/pii-key value="NEW_ROTATED_KEY_VALUE"
vault kv get secret/pii-key   # confirms version 2
```

Re-encrypt existing data with the new key:

```sql
-- TODO: Write an UPDATE statement that:
-- 1. Decrypts using the OLD key
-- 2. Re-encrypts using the NEW key
-- Hint: nest pgp_sym_decrypt inside pgp_sym_encrypt
UPDATE customers
SET national_id_encrypted = pgp_sym_encrypt(
    pgp_sym_decrypt(national_id_encrypted, 'OLD_KEY'),
    'NEW_ROTATED_KEY_VALUE'
);
```

Verify the ciphertext bytes changed even though plaintext is identical:

```sql
SELECT id, encode(national_id_encrypted, 'hex') FROM customers;
```

- Compare hex output before and after rotation — they must differ
- Confirm old key no longer decrypts correctly (should throw error or garbage output):

```sql
-- TODO: Attempt decryption with the OLD key and observe the failure
```

> ✅ **Checkpoint:** Document the timestamp of rotation and confirm previous ciphertext is no longer valid with the old key.

---

## 📋 Task 5: Map Controls to PDPL/GDPR Articles

Create a file documenting your controls:

```bash
nano compliance_mapping.md
```

Include a table like this (fill in based on what you configured):

| Control Implemented | Technical Mechanism | GDPR Article 32 Reference | GCC PDPL Reference |
|---|---|---|---|
| Encryption at rest | LUKS full-disk encryption | Art. 32(1)(a) — encryption of personal data | e.g., UAE PDPL Art. 20, KSA PDPL Art. 19 |
| Field-level encryption | pgcrypto `pgp_sym_encrypt`/`decrypt` | Art. 32(1)(a) | Data minimization/security articles |
| Key management | Vault KV secrets engine | Art. 32(1)(b) — confidentiality/integrity | Key custodian requirements |
| Key rotation | Vault versioned secrets + re-encryption | Art. 32(1)(d) — regular testing/evaluation | Periodic security review clauses |

> **TODO:** Research your target jurisdiction (KSA PDPL, UAE PDPL, or Bahrain PDPL) and fill in the exact article numbers.

---

## ✅ Verification

Run through this checklist on your machine:

```bash
# 1️⃣ Confirm LUKS volume is active
sudo cryptsetup status secure_pgdata

# 2️⃣ Confirm PostgreSQL tablespace is on encrypted volume
sudo -u postgres psql -c "\db+"

# 3️⃣ Confirm pgcrypto extension is active
sudo -u postgres psql -d privacy_db -c "\dx"

# 4️⃣ Confirm Vault is running and secret exists
vault kv get secret/pii-key

# 5️⃣ Confirm compliance_mapping.md exists and is completed
cat compliance_mapping.md
```

**Expected outcome:** All five checks should return valid, non-error output.

---

## 🔧 Troubleshooting

<details>
<summary>Click to expand common issues and fixes</summary>

| Issue | Fix |
|---|---|
| LUKS format fails "device is in use" | Run `sudo losetup -d /dev/loopX` and retry setup from Task 1 |
| Vault dev server not reachable | Confirm `VAULT_ADDR` is exported in the current shell session |
| pgcrypto function not found | Re-run `CREATE EXTENSION pgcrypto;` inside the correct database |
| Decryption returns error | Verify you're using the exact key string (case-sensitive) stored in Vault |

</details>

---

## 🎯 MITRE ATT&CK Mapping

| Technique ID | Technique | Relevance |
|---|---|---|
| T1552 | Unsecured Credentials | Hardcoded encryption keys (e.g. `REPLACE_WITH_KEY`) represent the exposure this lab's Vault workflow eliminates |
| T1552.001 | Credentials In Files | Sourcing the pgcrypto key from Vault rather than a config file or script prevents credential exposure |
| T1078 | Valid Accounts | Vault's root token and authenticated sessions gate who can retrieve the encryption key |
| T1005 | Data from Local System | LUKS full-disk encryption protects PostgreSQL data files from unauthorized local disk access |

---

## 🏁 Conclusion

### 🎉 Key Accomplishments
- Built a layered data-at-rest protection strategy: disk-level encryption using LUKS and field-level encryption of PII using PostgreSQL's pgcrypto extension
- Deployed centralized key lifecycle management using HashiCorp Vault
- Performed a key rotation exercise and confirmed ciphertext changes as proof of effective key management
- Documented how each technical control maps to GDPR Article 32 and GCC PDPL security requirements

### 💼 Real-World Applications
This is a critical skill for **Security Engineers** supporting compliance audits and technical control assessments under **CISSP** and **ISO 27001** frameworks.

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Education-blue?style=for-the-badge)

</div>
