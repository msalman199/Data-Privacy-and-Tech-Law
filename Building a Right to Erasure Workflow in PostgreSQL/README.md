# 🛡️ Building a Right to Erasure Workflow in PostgreSQL

> 🔐 A hands-on privacy engineering lab demonstrating a complete **Right to Erasure workflow** using PostgreSQL, Python, audit logging, backup anonymization, and GDPR Article 17 concepts.

---

## 🎯 Objectives

By completing this lab, you will be able to:

* 🗄️ Design a multi-table PostgreSQL schema representing user data.
* 🔎 Build a Python service that traces records associated with a data subject.
* 🟡 Implement a soft-delete followed by hard-delete workflow.
* 📋 Maintain an audit trail for deletion activities.
* 💾 Simulate backup anonymization for retained data copies.
* 🧾 Generate an erasure confirmation certificate.
* 🛡️ Apply practical privacy-by-design principles.

---

## 🛠️ Technologies Used

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![Python](https://img.shields.io/badge/Python-Backend_Service-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Database_Operations-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Lab_Environment-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge\&logo=git\&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-Article_17-8B0000?style=for-the-badge)

---

## 📋 Prerequisites

* 🐧 Basic Linux terminal knowledge
* 🗃️ Basic SQL knowledge
* 🔗 Understanding of JOINs and foreign keys
* 🔄 Understanding of database transactions
* 🐍 Basic Python knowledge
* 🔌 Familiarity with `psycopg2`
* 🛡️ Basic understanding of GDPR Article 17

---

# 🚀 Step 1 — Environment Setup

Update the package repository:

```bash
sudo apt update
```

Install PostgreSQL and required packages:

```bash
sudo apt install -y postgresql postgresql-contrib python3-pip
```

Install Python dependencies:

```bash
pip3 install psycopg2-binary faker
```

Start PostgreSQL:

```bash
sudo systemctl start postgresql
```

Enable PostgreSQL:

```bash
sudo systemctl enable postgresql
```

Verify the service:

```bash
sudo systemctl status postgresql
```

✅ Expected status:

```text
active (running)
```

---

# 🗄️ Step 2 — Create Database and User

Create the database:

```bash
sudo -u postgres psql -c "CREATE DATABASE erasure_lab;"
```

Create the database user:

```bash
sudo -u postgres psql -c "CREATE USER lab_user WITH PASSWORD 'labpass123';"
```

Grant privileges:

```bash
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE erasure_lab TO lab_user;"
```

Connect to PostgreSQL:

```bash
psql -h localhost -U lab_user -d erasure_lab
```

---

# 🧱 Step 3 — Create the Multi-Table Dataset

Create the `users` table:

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP
);
```

Create the `orders` table:

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    amount NUMERIC(10,2),
    order_date TIMESTAMP DEFAULT NOW()
);
```

Create the `support_tickets` table:

```sql
CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Create the audit table:

```sql
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    user_id INT,
    action VARCHAR(50),
    table_name VARCHAR(50),
    performed_at TIMESTAMP DEFAULT NOW(),
    details JSONB
);
```

Create the simulated backup:

```sql
CREATE TABLE users_backup (LIKE users INCLUDING ALL);
```

---

# 👥 Step 4 — Insert Sample Data

Insert users:

```sql
INSERT INTO users (email, full_name) VALUES
('alice@example.com', 'Alice Khan'),
('bob@example.com', 'Bob Ahmed');
```

Insert orders:

```sql
INSERT INTO orders (user_id, amount)
VALUES
(1, 250.00),
(1, 99.50),
(2, 40.00);
```

Insert support tickets:

```sql
INSERT INTO support_tickets (user_id, message)
VALUES
(1, 'Refund request'),
(2, 'Login issue');
```

Populate the backup:

```sql
INSERT INTO users_backup
SELECT * FROM users;
```

Exit PostgreSQL:

```sql
\q
```

### 🔎 Checkpoint

Run:

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT COUNT(*) FROM users;"
```

Expected:

```text
2
```

---

# 🐍 Step 5 — Build the Python Service

Create the Python file:

```bash
nano erasure_service.py
```

Configure the database connection:

```python
import psycopg2
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "dbname": "erasure_lab",
    "user": "lab_user",
    "password": "labpass123"
}

RELATED_TABLES = ["orders", "support_tickets"]

def get_connection():
    return psycopg2.connect(**DB_CONFIG)
```

The service will locate the user and associated records across the database.

---

# 🔎 Step 6 — Locate Related Records

Implement:

```python
def find_user_records(email: str) -> dict:
    """
    Locate the user and all related records.
    """
```

Use parameterized SQL queries:

```python
cursor.execute(
    "SELECT user_id FROM users WHERE email = %s",
    (email,)
)
```

Example result:

```python
{
    "user_id": 1,
    "records": {
        "orders": 2,
        "support_tickets": 1
    }
}
```

### 🔐 Security

Use parameterized queries instead of directly inserting user input into SQL statements.

---

# 🟡 Step 7 — Implement Soft Delete

Implement:

```python
def soft_delete_user(user_id: int):
    """
    Mark a user as deleted and record the operation.
    """
```

Update the user:

```sql
UPDATE users
SET is_deleted = TRUE,
    deleted_at = NOW()
WHERE user_id = %s;
```

Record the operation:

```text
SOFT_DELETE
```

Commit the transaction:

```python
conn.commit()
```

---

# 🔴 Step 8 — Implement Hard Delete

Delete related records before deleting the user:

```text
orders
    ↓
support_tickets
    ↓
users
```

Each deletion must be recorded in `audit_log`.

Example actions:

```text
HARD_DELETE → orders
HARD_DELETE → support_tickets
HARD_DELETE → users
```

---

# 🔄 Step 9 — Implement Transaction Handling

All hard-delete operations must use one transaction.

```python
try:
    # Delete records
    conn.commit()

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
```

### 🛡️ Transaction Flow

```text
BEGIN
  │
  ├── Delete orders
  ├── Audit deletion
  ├── Delete support tickets
  ├── Audit deletion
  ├── Delete user
  └── Audit deletion
  │
  ▼
COMMIT
```

If any operation fails:

```text
ERROR ❌
   │
   ▼
ROLLBACK 🔄
```

---

# 📋 Step 10 — Verify Audit Logging

Run:

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT * FROM audit_log;"
```

You should see multiple entries documenting the deletion workflow.

---

# 💾 Step 11 — Anonymize Backup Data

Implement:

```python
def anonymize_backup(user_id: int, original_email: str):
    """
    Anonymize the user's record in backup storage.
    """
```

Update the backup record:

```sql
UPDATE users_backup
SET
    email = CONCAT('anon_', user_id, '@erased.local'),
    full_name = 'REDACTED'
WHERE user_id = %s;
```

Record the operation:

```text
ANONYMIZE_BACKUP
```

---

# ✅ Step 12 — Verify Backup Anonymization

Implement:

```python
def verify_backup_anonymized(user_id: int) -> bool:
    """
    Confirm no identifiable PII remains.
    """
```

Run:

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT email, full_name FROM users_backup WHERE user_id=1;"
```

Expected:

```text
anon_1@erased.local | REDACTED
```

---

# 🧾 Step 13 — Generate Erasure Certificate

Implement:

```python
def generate_certificate(user_id: int, email: str) -> str:
    """
    Generate an erasure confirmation certificate.
    """
```

Hash the email:

```python
import hashlib

subject_hash = hashlib.sha256(
    email.encode()
).hexdigest()
```

Generate:

```text
certificate_<user_id>.txt
```

The certificate should include:

* 📜 Certificate title
* 🔐 Hashed subject reference
* 🕐 Timestamp
* 📋 Actions performed
* 🗃️ Affected tables
* 🛡️ GDPR Article 17 statement

---

# 🧪 Step 14 — Run the Complete Workflow

Run the complete process:

```python
info = find_user_records("bob@example.com")

soft_delete_user(info["user_id"])

hard_delete_user(info["user_id"])

anonymize_backup(
    info["user_id"],
    "bob@example.com"
)

cert_path = generate_certificate(
    info["user_id"],
    "bob@example.com"
)

print(f"Certificate created: {cert_path}")
```

---

# 🔍 Step 15 — Verification

### 👤 Verify User Deletion

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT * FROM users WHERE email='bob@example.com';"
```

Expected:

```text
0 rows
```

### 🛒 Verify Orders

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT * FROM orders WHERE user_id=2;"
```

Expected:

```text
0 rows
```

### 💾 Verify Backup

```bash
psql -h localhost -U lab_user -d erasure_lab \
-c "SELECT email, full_name FROM users_backup WHERE user_id=2;"
```

Expected:

```text
anon_2@erased.local | REDACTED
```

### 🧾 Verify Certificate

```bash
cat certificate_2.txt
```

Expected:

```text
Hashed subject reference
Audit summary
Erasure timestamp
GDPR Article 17 statement
```

---

# 🏗️ Workflow Architecture

```text
                 👤 DATA SUBJECT
                       │
                       ▼
                🔎 FIND RECORDS
                       │
                       ▼
                🟡 SOFT DELETE
                       │
                       ▼
                🔴 HARD DELETE
                       │
                       ▼
                📋 AUDIT LOG
                       │
                       ▼
             💾 BACKUP ANONYMIZATION
                       │
                       ▼
                 ✅ VERIFICATION
                       │
                       ▼
               🧾 CERTIFICATE
```

---

# 🛠️ Troubleshooting

### ❌ Foreign Key Violation

Delete child records before deleting the parent:

```text
orders
support_tickets
      ↓
users
```

---

### ❌ PostgreSQL Connection Refused

Check PostgreSQL:

```bash
sudo systemctl status postgresql
```

Start it:

```bash
sudo systemctl start postgresql
```

---

### ❌ Transaction Error

Use:

```python
conn.commit()
```

for successful operations and:

```python
conn.rollback()
```

when an exception occurs.

---

# 📊 Skills Demonstrated

| 🛠️ Skill              | 🎯 Demonstration                  |
| ---------------------- | --------------------------------- |
| 🐘 PostgreSQL          | Relational database design        |
| 🐍 Python              | Erasure automation service        |
| 🗃️ SQL                | CRUD and transactional operations |
| 🔐 Privacy Engineering | Data erasure workflow             |
| 🛡️ GDPR               | Article 17 concepts               |
| 📋 Audit Logging       | Traceable deletion operations     |
| 💾 Backup Management   | Backup anonymization              |
| 🔄 Transactions        | Consistent database operations    |
| 🔒 Secure Coding       | Parameterized SQL                 |
| 🐧 Linux               | PostgreSQL environment setup      |

---

# 🎓 Learning Outcomes

After completing this lab, you will be able to:

* ✅ Design a multi-table PostgreSQL dataset.
* ✅ Trace data belonging to a specific user.
* ✅ Build a Python PostgreSQL service.
* ✅ Implement soft deletion.
* ✅ Implement permanent deletion.
* ✅ Maintain an audit trail.
* ✅ Handle database transactions safely.
* ✅ Anonymize retained backup data.
* ✅ Verify successful erasure.
* ✅ Generate an erasure certificate.
* ✅ Apply practical GDPR Article 17 concepts.

---

# 🏆 Final Workflow

```text
🔎 Data Discovery
       ↓
🟡 Soft Delete
       ↓
🔴 Hard Delete
       ↓
📋 Audit Logging
       ↓
💾 Backup Anonymization
       ↓
🔍 Verification
       ↓
🧾 Erasure Certificate
       ↓
✅ COMPLETED
```

---

## 👨‍💻 Author

**Hafiz Muhammad Salman**

☁️ Cloud DevOps Engineer | 🐧 Linux Administrator

---

## ⭐ Conclusion

This hands-on lab combines **PostgreSQL, Python, SQL, privacy engineering, audit logging, transactional database operations, backup anonymization, and GDPR Article 17 concepts** into a practical Right to Erasure workflow.

**🔐 Secure Data • 🛡️ Protect Privacy • 📋 Maintain Accountability • 🚀 Keep Learning**
