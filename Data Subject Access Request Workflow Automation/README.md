<div align="center">

# 📨 Data Subject Access Request Workflow Automation

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-003399?style=for-the-badge&logo=europeanunion&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

*Build a functional DSAR intake, verification, and compliance-reporting pipeline*

</div>

---

## 📖 Table of Contents

- [🎯 Objectives](#-objectives)
- [📋 Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🎫 Task 1: Set Up Local Ticketing System](#-task-1-set-up-local-ticketing-system)
- [📄 Task 2: Define DSAR Templates](#-task-2-define-dsar-templates)
- [🔐 Task 3: Identity Verification via OTP + Local SMTP](#-task-3-identity-verification-via-otp--local-smtp)
- [📦 Task 4: Generate JSON Portability Bundle](#-task-4-generate-json-portability-bundle)
- [⏱️ Task 5: SLA Tracking and Compliance Report](#️-task-5-sla-tracking-and-compliance-report)
- [✅ Verification](#-verification)
- [🔧 Troubleshooting](#-troubleshooting)
- [🔑 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Objectives

| # | By completing this lab, you will... |
|---|---|
| 1 | Deploy a local ticketing system to intake DSAR requests |
| 2 | Create structured DSAR templates for access, deletion, and portability rights |
| 3 | Implement OTP-based identity verification using local SMTP |
| 4 | Build a script to generate JSON data portability bundles from a database |
| 5 | Track SLA compliance timers and generate a compliance report |

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| Linux CLI | Basic — file editing, permissions, package management |
| Python 3 | Basic — functions, JSON, file I/O |
| SQL/SQLite | Basic familiarity |
| GDPR knowledge | Understanding of data subject rights (Access, Rectification, Erasure, Portability) |
| Docker | Helpful but not required |

## 🖥️ Lab Environment

> A single Linux machine (Ubuntu 22.04+) is provided via **Start Lab**.

```bash
# 📦 Install required packages
sudo apt update
sudo apt install -y docker.io docker-compose python3 python3-pip sqlite3 mailutils
sudo systemctl start docker
pip3 install pyotp
```

---

## 🎫 Task 1: Set Up Local Ticketing System

> Zammad requires significant resources; for this lab we use a lightweight alternative — a local SQLite-backed Flask app simulating a Django-based ticket system (faster to provision, same workflow concepts).

```bash
# 📁 Create project directory
mkdir -p ~/dsar-lab/{tickets,scripts,templates,reports}
cd ~/dsar-lab
```

```bash
# 🗄️ Create the ticket intake database schema
sqlite3 tickets/dsar.db <<EOF
CREATE TABLE requests (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject_email TEXT NOT NULL,
  request_type TEXT NOT NULL,
  status TEXT DEFAULT 'received',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sla_deadline TIMESTAMP,
  verified INTEGER DEFAULT 0
);
EOF
```

Complete the intake script `scripts/intake.py`:

```python
import sqlite3
from datetime import datetime, timedelta

DB_PATH = "tickets/dsar.db"
SLA_DAYS = 30  # GDPR standard; adjust for PDPL if needed

def create_request(email: str, request_type: str) -> int:
    """
    Insert a new DSAR ticket into the database.

    Args:
        email: Data subject's email address
        request_type: One of 'access', 'deletion', 'portability', 'rectification'

    Returns:
        The new request ID
    """
    # TODO: validate request_type against allowed values
    # TODO: calculate sla_deadline = now + SLA_DAYS
    # TODO: insert row into requests table
    # TODO: return the new row's id
    pass

if __name__ == "__main__":
    # TODO: call create_request() with sample data and print the ID
    pass
```

Run and verify a row is created:

```bash
python3 scripts/intake.py
sqlite3 tickets/dsar.db "SELECT * FROM requests;"
```

---

## 📄 Task 2: Define DSAR Templates

Create three template files under `templates/`.

**Requirements:**
- `templates/access_template.txt` — must include: requester identity fields, scope of data requested, response deadline, verification status placeholder
- `templates/deletion_template.txt` — must include: confirmation of erasure scope, legal basis for retention exceptions, deletion completion date
- `templates/portability_template.txt` — must include: data format (JSON), transfer method, checksum for integrity

**Task:** Write each template with at least 5 placeholder fields (e.g., `{{subject_name}}`, `{{request_date}}`). Reference the IAPP CIPM body of knowledge on data subject rights for required fields.

---

## 🔐 Task 3: Identity Verification via OTP + Local SMTP

Configure a local SMTP debug server (no external mail server needed):

```bash
python3 -m smtpd -c DebuggingServer -n localhost:1025 &
```

Complete `scripts/verify_otp.py`:

```python
import pyotp
import smtplib
from email.mime.text import MIMEText

def generate_otp(secret: str) -> str:
    """
    Generate a time-based OTP using the provided secret.

    Args:
        secret: Base32 secret key

    Returns:
        6-digit OTP string
    """
    # TODO: use pyotp.TOTP to generate current OTP
    pass

def send_otp_email(to_email: str, otp: str) -> None:
    """
    Send the OTP to the data subject via local SMTP (localhost:1025).

    Args:
        to_email: Recipient email address
        otp: The OTP code to send
    """
    # TODO: build MIMEText message with OTP
    # TODO: connect to smtplib.SMTP("localhost", 1025)
    # TODO: send message and close connection
    pass

def verify_otp(secret: str, user_input: str) -> bool:
    """
    Verify the OTP entered by the user against the secret.
    """
    # TODO: use pyotp.TOTP(secret).verify(user_input)
    pass

if __name__ == "__main__":
    secret = pyotp.random_base32()
    otp = generate_otp(secret)
    send_otp_email("subject@example.com", otp)
    print(f"OTP sent. Secret (for testing): {secret}")
```

- Run the script and confirm the SMTP debug server console prints the email content
- Test verification logic manually by re-running `verify_otp()` with the printed OTP

---

## 📦 Task 4: Generate JSON Portability Bundle

```bash
# 🗄️ Create a sample customer database
sqlite3 tickets/customer.db <<EOF
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, address TEXT, signup_date TEXT);
INSERT INTO customers VALUES (1, 'Ahmed Ali', 'ahmed@example.com', 'Dubai, UAE', '2022-01-15');
EOF
```

Complete `scripts/export_portability.py`:

```python
import sqlite3
import json
import hashlib

def fetch_customer_data(email: str) -> dict:
    """
    Query customer.db for all records matching the given email.

    Returns:
        Dictionary of customer fields
    """
    # TODO: connect to tickets/customer.db
    # TODO: query row matching email
    # TODO: convert row to dict and return
    pass

def build_json_bundle(data: dict, output_path: str) -> str:
    """
    Write data to a JSON file and return a SHA-256 checksum of the file.

    Args:
        data: Customer data dictionary
        output_path: File path to write JSON bundle

    Returns:
        Hex checksum string
    """
    # TODO: write data as formatted JSON to output_path
    # TODO: compute sha256 hash of the file contents
    # TODO: return hex digest
    pass

if __name__ == "__main__":
    data = fetch_customer_data("ahmed@example.com")
    checksum = build_json_bundle(data, "reports/portability_bundle.json")
    print(f"Bundle created. Checksum: {checksum}")
```

- Run the script and inspect `reports/portability_bundle.json`

---

## ⏱️ Task 5: SLA Tracking and Compliance Report

Complete `scripts/sla_report.py`:

```python
import sqlite3
from datetime import datetime

def get_overdue_requests(db_path: str = "tickets/dsar.db") -> list:
    """
    Return all requests where sla_deadline has passed and status != 'completed'.
    """
    # TODO: query requests table for overdue, non-completed rows
    pass

def generate_report(db_path: str = "tickets/dsar.db", output_path: str = "reports/compliance_report.txt") -> None:
    """
    Write a summary report: total requests, completed, overdue, and
    percentage compliance (completed within SLA / total).
    """
    # TODO: query totals from the requests table
    # TODO: calculate compliance percentage
    # TODO: write formatted summary to output_path
    pass

if __name__ == "__main__":
    generate_report()
    print("Report generated at reports/compliance_report.txt")
```

- Run the script and review `reports/compliance_report.txt`

---

## ✅ Verification

Confirm the following on your lab machine:

```bash
# 1️⃣ Ticket exists in database
sqlite3 tickets/dsar.db "SELECT id, request_type, status FROM requests;"

# 2️⃣ Templates exist
ls templates/*.txt

# 3️⃣ OTP script runs without error
python3 scripts/verify_otp.py

# 4️⃣ Portability bundle and checksum exist
cat reports/portability_bundle.json
sha256sum reports/portability_bundle.json

# 5️⃣ Compliance report generated
cat reports/compliance_report.txt
```

**Expected outcome:** Each command should return non-empty, valid output matching the task descriptions above.

---

## 🔧 Troubleshooting

<details>
<summary>Click to expand common issues and fixes</summary>

| Issue | Fix |
|---|---|
| SMTP connection refused | Ensure the `python3 -m smtpd` process is still running (`jobs` or `ps aux \| grep smtpd`) |
| `pyotp` import error | Re-run `pip3 install pyotp` |
| SQLite "database is locked" | Close any open `sqlite3` shell sessions before running scripts |
| Empty query results | Double-check email strings match exactly (case-sensitive) between scripts and inserted data |

</details>

---

## 🔑 Key Concepts

| Concept | Description |
|---|---|
| DSAR | Data Subject Access Request — a formal request to exercise GDPR data subject rights |
| SLA Tracking | Monitoring response deadlines (e.g., 30-day GDPR standard) against ticket status |
| OTP-Based Identity Verification | Confirming a requester's identity before releasing personal data |
| Data Portability | Exporting a subject's data in a structured, machine-readable format (JSON) |
| Checksum Integrity | Using a SHA-256 hash to verify a data export hasn't been altered |
| GDPR Articles 15-20 | The regulatory basis for access, rectification, erasure, and portability rights |

---

## 🏁 Conclusion

### 🎉 Key Accomplishments
- Built a functional DSAR workflow pipeline on a single Linux machine
- Implemented intake ticketing, rights-specific templates, and OTP-based identity verification over local SMTP
- Produced JSON-based data portability export with integrity checksums
- Generated an SLA compliance report

### 💼 Real-World Applications
These components map directly to operational requirements under **GDPR Articles 15-20** and equivalent **GCC PDPL** provisions, giving practical experience relevant to the **Privacy Operations Analyst** role and IAPP **CIPM** competency areas around operationalizing data subject rights.

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Education-blue?style=for-the-badge)

</div>
