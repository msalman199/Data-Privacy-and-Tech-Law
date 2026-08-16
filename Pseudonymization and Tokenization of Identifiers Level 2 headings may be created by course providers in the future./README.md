<div align="center">

# 🔒 Pseudonymization and Tokenization of Identifiers

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-003399?style=for-the-badge&logo=europeanunion&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

*Build format-preserving tokenization with an isolated vault and an authorized reidentification path*

</div>

---

## 📖 Table of Contents

- [🎯 Objectives](#-objectives)
- [📋 Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🗄️ Task 1: Load Sample Dataset with Emirates IDs](#️-task-1-load-sample-dataset-with-emirates-ids)
- [🔑 Task 2: Implement Format-Preserving Tokenization](#-task-2-implement-format-preserving-tokenization)
- [🗝️ Task 3: Store Token Vault with Restrictive Permissions](#️-task-3-store-token-vault-with-restrictive-permissions)
- [🔓 Task 4: Reidentify a Record via Authorized Access](#-task-4-reidentify-a-record-via-authorized-access)
- [📝 Task 5: Document Residual Risk and Key Management Controls](#-task-5-document-residual-risk-and-key-management-controls)
- [✅ Verification](#-verification)
- [🔧 Troubleshooting](#-troubleshooting)
- [🎯 MITRE ATT&CK Mapping](#-mitre-attck-mapping)
- [🔑 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Objectives

| # | By the end of this lab, you will be able to... |
|---|---|
| 1 | Load and manage sensitive identifier data (Emirates IDs) in PostgreSQL |
| 2 | Implement format-preserving tokenization using Python |
| 3 | Separate token vaults from operational data with restrictive file/database permissions |
| 4 | Perform controlled reidentification through an authorized access path |
| 5 | Document residual risk and key management controls aligned with GDPR Art. 32 and GCC PDPL |

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| SQL | Basic — `INSERT`, `SELECT`, `GRANT`/`REVOKE` |
| Python | Basic — functions, dictionaries, file I/O |
| Linux file permissions | Familiarity with `chmod`, `chown` |
| Privacy concepts | Understanding of pseudonymization vs. anonymization |

## 🖥️ Lab Environment

> Your Al Nafi Linux machine comes with a terminal.

```bash
# 📦 Install required packages
sudo apt update
sudo apt install -y postgresql postgresql-contrib python3-pip
sudo systemctl start postgresql
sudo systemctl enable postgresql
pip3 install psycopg2-binary cryptography
```

```bash
# 🗄️ Create a database and working user
sudo -u postgres psql -c "CREATE DATABASE privacy_lab;"
sudo -u postgres psql -c "CREATE USER lab_app WITH PASSWORD 'LabPass123';"
sudo -u postgres psql -d privacy_lab -c "GRANT CONNECT ON DATABASE privacy_lab TO lab_app;"
```

---

## 🗄️ Task 1: Load Sample Dataset with Emirates IDs

> Emirates ID format: `784-YYYY-NNNNNNN-C` (15 digits total).

Create the schema and load sample data:

```sql
sudo -u postgres psql -d privacy_lab

CREATE SCHEMA raw_data;

CREATE TABLE raw_data.customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    emirates_id VARCHAR(20) NOT NULL,
    phone VARCHAR(15)
);

INSERT INTO raw_data.customers (full_name, emirates_id, phone) VALUES
('Ahmed Al Mansoori', '784-1990-1234567-1', '0501234567'),
('Fatima Al Suwaidi', '784-1985-7654321-2', '0559876543'),
('Sara Khan', '784-1992-1112223-4', '0521112233');

GRANT USAGE ON SCHEMA raw_data TO lab_app;
GRANT SELECT ON raw_data.customers TO lab_app;
\q
```

> ✅ **Checkpoint:** Confirm 3 rows exist: `SELECT count(*) FROM raw_data.customers;`

---

## 🔑 Task 2: Implement Format-Preserving Tokenization

> Format-preserving tokenization replaces the digits of the Emirates ID with a deterministic pseudonymous value of the same length/pattern, while the mapping is stored separately.

Create `tokenize.py`:

```python
import psycopg2
import hmac
import hashlib
import os
import json

SECRET_KEY = os.urandom(32)  # TODO: In production, load from a secure key store, not memory

def format_preserving_token(emirates_id: str, key: bytes) -> str:
    """
    Generate a format-preserving token for an Emirates ID.
    Keeps the '784-YYYY-' prefix structure but replaces
    the last 7 digits + check digit with a deterministic pseudonymous number.

    Args:
        emirates_id: Original ID, e.g. '784-1990-1234567-1'
        key: Secret key for HMAC generation

    Returns:
        Tokenized ID string in the same format
    """
    # TODO: Split emirates_id into prefix (784-YYYY-) and suffix (NNNNNNN-C)
    # TODO: Compute HMAC-SHA256 of the suffix using `key`
    # TODO: Convert HMAC digest into an 8-digit numeric string (mod 10**8)
    # TODO: Reconstruct token in format: 784-YYYY-<7digits>-<1digit>
    pass


def build_token_vault(records: list) -> dict:
    """
    Build a mapping of token -> original emirates_id (the vault).

    Args:
        records: list of tuples (customer_id, emirates_id)

    Returns:
        Dictionary {token: {"customer_id": id, "original_id": emirates_id}}
    """
    # TODO: Loop through records, call format_preserving_token()
    # TODO: Populate and return the vault dictionary
    pass


def fetch_customers(conn) -> list:
    """Fetch customer_id and emirates_id from raw_data.customers."""
    # TODO: Execute SELECT customer_id, emirates_id FROM raw_data.customers
    # TODO: Return list of tuples
    pass


if __name__ == "__main__":
    conn = psycopg2.connect(dbname="privacy_lab", user="lab_app",
                             password="LabPass123", host="localhost")

    # TODO: Call fetch_customers(conn)
    # TODO: Call build_token_vault() on the fetched records
    # TODO: Save vault to 'vault.json' (this file must later get restrictive permissions)
    # TODO: Save key to 'vault.key' (binary write)

    conn.close()
```

Run and verify:

```bash
python3 tokenize.py
cat vault.json
```

> 💡 **Hint:** Use `emirates_id.split('-')` and `hmac.new(key, suffix.encode(), hashlib.sha256).hexdigest()`. Convert hex to int with `int(digest, 16) % 10**8`.

---

## 🗝️ Task 3: Store Token Vault with Restrictive Permissions

> The vault (mapping + key) must be isolated from the pseudonymized dataset.

```bash
# 🗝️ Isolate the vault with restrictive permissions
mkdir -p ~/secure_vault
mv vault.json vault.key ~/secure_vault/
chmod 700 ~/secure_vault
chmod 600 ~/secure_vault/vault.json ~/secure_vault/vault.key
ls -la ~/secure_vault
```

Create a separate PostgreSQL table to store only tokens (no vault access):

```sql
sudo -u postgres psql -d privacy_lab

CREATE SCHEMA pseudonymized;

CREATE TABLE pseudonymized.customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    emirates_id_token VARCHAR(20),
    phone VARCHAR(15)
);

-- TODO: Restrict access so only a dedicated 'reidentify_role' can join tokens back to the vault
CREATE ROLE reidentify_role LOGIN PASSWORD 'ReidPass123';
GRANT SELECT ON pseudonymized.customers TO lab_app;
-- Do NOT grant reidentify_role access to raw_data schema
\q
```

Load your tokenized records into `pseudonymized.customers` using a Python insert loop (extend `tokenize.py` or write a new script `load_tokens.py`) — insert `customer_id`, `full_name`, the generated token, and `phone`.

> ✅ **Checkpoint:** `SELECT * FROM pseudonymized.customers;` should show tokens, not real Emirates IDs.

---

## 🔓 Task 4: Reidentify a Record via Authorized Access

Create `reidentify.py` — this script represents the only authorized path back to real identifiers.

```python
import json

VAULT_PATH = "/home/<your_user>/secure_vault/vault.json"  # TODO: update path

def reidentify_token(token: str, vault_path: str) -> dict:
    """
    Look up the original Emirates ID for a given token.
    Simulates an authorized privileged-access workflow.

    Args:
        token: The pseudonymized identifier
        vault_path: Path to the restricted vault file

    Returns:
        Dict with original_id and customer_id, or an error message
    """
    # TODO: Open and load the vault JSON file
    # TODO: Search for matching token key
    # TODO: Return the associated record, or {"error": "Token not found"}
    pass


if __name__ == "__main__":
    test_token = input("Enter token to reidentify: ")
    result = reidentify_token(test_token, VAULT_PATH)
    print(result)
```

Test with a token from `pseudonymized.customers`:

```bash
python3 reidentify.py
```

- **Access control test:** Try reading `vault.json` as a non-owner user (or via `sudo -u lab_app cat ~/secure_vault/vault.json`) — it should fail with permission denied, proving separation of duties

---

## 📝 Task 5: Document Residual Risk and Key Management Controls

Create `risk_documentation.md` and answer the following (2-3 sentences each):

1. **Residual Re-identification Risk** — Even with tokenization, what residual risk remains (e.g., vault compromise, HMAC key leakage, small keyspace attacks on 8-digit tokens)?
2. **Key Management** — Where should `vault.key` actually be stored in production (e.g., HSM, KMS, HashiCorp Vault) instead of a local file?
3. **Access Control Mapping** — Which role(s) should be permitted to run `reidentify.py`, and how does this map to GDPR Art. 32 (security of processing) and GCC PDPL data minimization principles?
4. **Separation of Duties** — Explain why `raw_data`, `pseudonymized`, and the vault are kept in different schemas/locations

---

## ✅ Verification

Confirm lab completion with these checks:

```bash
# 1️⃣ Raw data exists
sudo -u postgres psql -d privacy_lab -c "SELECT count(*) FROM raw_data.customers;"

# 2️⃣ Tokens generated and stored separately
sudo -u postgres psql -d privacy_lab -c "SELECT emirates_id_token FROM pseudonymized.customers;"

# 3️⃣ Vault permissions are restrictive
stat -c "%a %n" ~/secure_vault/vault.json   # expect 600

# 4️⃣ Reidentification script works
python3 reidentify.py

# 5️⃣ Documentation exists
cat risk_documentation.md
```

---

## 🔧 Troubleshooting

<details>
<summary>Click to expand common issues and fixes</summary>

| Issue | Fix |
|---|---|
| `psycopg2` connection refused | Check `pg_hba.conf` allows md5/scram-sha-256 for local connections; restart PostgreSQL |
| Permission denied on vault | Confirm you're testing as a different OS user than the file owner |
| Token length mismatch | Ensure your modulo operation always zero-pads to 8 digits (`str(num).zfill(8)`) |

</details>

---

## 🎯 MITRE ATT&CK Mapping

| Technique ID | Technique | Relevance |
|---|---|---|
| T1552 | Unsecured Credentials | Vault key/mapping left in plaintext or with weak permissions could expose reidentification capability |
| T1552.001 | Credentials In Files | `vault.key` and `vault.json` are file-based secrets requiring restrictive permissions |
| T1078 | Valid Accounts | `reidentify_role` represents the sole authorized identity permitted to reverse tokenization |
| T1005 | Data from Local System | Unauthorized local access to the vault file would expose the original Emirates IDs |

---

## 🔑 Key Concepts

| Concept | Description |
|---|---|
| Pseudonymization vs. Anonymization | Pseudonymized data can be reversed with the right key/vault; anonymized data cannot |
| Format-Preserving Tokenization | Replacing identifier digits with a deterministic token that keeps the original structure |
| Token Vault Separation | Isolating the token-to-identifier mapping from operational/pseudonymized data |
| Separation of Duties | Restricting reidentification capability to a single dedicated role |
| Key Management | Where and how the HMAC secret key should be stored and protected |
| GDPR Art. 32 / GCC PDPL | The regulatory basis for security of processing and data minimization |

---

## 🏁 Conclusion

### 🎉 Key Accomplishments
- Built an end-to-end pseudonymization workflow: loading sensitive Emirates ID data into PostgreSQL and implementing format-preserving tokenization in Python
- Physically/logically separated the token vault using Linux file permissions and database schema isolation
- Simulated an authorized reidentification path
- Documented residual risks and key management controls

### 💼 Real-World Applications
These practices directly support **GDPR Article 32** security safeguards and **GCC PDPL** data minimization requirements, giving practical experience relevant to **Privacy Engineer** and **Data Engineer** roles and the IAPP **CIPT** body of knowledge.

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Education-blue?style=for-the-badge)

</div>
