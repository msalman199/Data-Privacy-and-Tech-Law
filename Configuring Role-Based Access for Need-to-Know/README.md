# 🔐 Configuring Role-Based Access for Need-to-Know

> 🛡️ A hands-on PostgreSQL security lab demonstrating **Role-Based Access Control (RBAC)**, column-level permissions, Row-Level Security (RLS), pgAudit logging, segregation of duties, and PDPL-aligned access management.

---

## 🎯 Objectives

By completing this lab, you will be able to:

* 👥 Create PostgreSQL roles for HR, Finance, and Audit functions.
* 🔒 Implement column-level access restrictions.
* 🧱 Implement Row-Level Security (RLS).
* 📋 Enable pgAudit for database activity monitoring.
* 🧪 Validate access boundaries by testing each role.
* ⚖️ Map the access-control model to PDPL principles.
* 🛡️ Apply least-privilege and need-to-know concepts.

---

# 🛠️ Technologies & Tools

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![pgAudit](https://img.shields.io/badge/pgAudit-Audit_Logging-336791?style=for-the-badge\&logo=postgresql\&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Access_Control-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Administration-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![RBAC](https://img.shields.io/badge/RBAC-Role_Based_Access_Control-6A1B9A?style=for-the-badge)
![RLS](https://img.shields.io/badge/RLS-Row_Level_Security-8B0000?style=for-the-badge)
![PDPL](https://img.shields.io/badge/PDPL-Data_Protection-00897B?style=for-the-badge)

---

# 📋 Prerequisites

Before starting, you should have:

* 🐧 Basic Linux command-line knowledge
* 🗃️ Basic SQL knowledge
* 👥 Understanding of roles and users
* 🔐 Understanding of least privilege
* 🛡️ Basic RBAC concepts
* 📊 Basic database security concepts

No previous pgAudit experience is required.

---

# 🏗️ Access Control Architecture

```text
                       🗄️ PostgreSQL
                            │
                  employee_records
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
   👤 HR Role         💰 Finance Role      📋 Audit Role
        │                   │                   │
        ▼                   ▼                   ▼
   All Columns        Limited Columns       Audit Columns
        │                   │                   │
        ▼                   ▼                   ▼
   All Employees       Finance Rows        Audit Rows
                            │
                            ▼
                       📋 pgAudit
                            │
                            ▼
                     🔍 Audit Logs
```

---

# 🚀 Step 1 — Install PostgreSQL

Update the package repository:

```bash id="j7nd4a"
sudo apt update
```

Install PostgreSQL:

```bash id="a6g12k"
sudo apt install -y postgresql postgresql-contrib
```

Install pgAudit:

```bash id="w3t8pp"
sudo apt install -y postgresql-15-pgaudit
```

> 💡 If your PostgreSQL version is different, install the pgAudit package matching your installed PostgreSQL version.

Start PostgreSQL:

```bash id="qz8t8s"
sudo systemctl start postgresql
```

Enable PostgreSQL at boot:

```bash id="g5ks8d"
sudo systemctl enable postgresql
```

---

# 🔎 Step 2 — Verify Installation

Check PostgreSQL:

```bash id="f5g3hv"
psql --version
```

Check the PostgreSQL server:

```bash id="t8n2bf"
sudo -u postgres psql -c "SELECT version();"
```

Expected output should show your PostgreSQL version.

---

# 🗄️ Step 3 — Create the Database

Create the lab database:

```bash id="d3ny9h"
sudo -u postgres createdb agency_records
```

Connect to it:

```bash id="k6qf3d"
sudo -u postgres psql -d agency_records
```

---

# 👥 Step 4 — Create RBAC Roles

Create the HR role:

```sql id="w3r0j8"
CREATE ROLE hr_role LOGIN PASSWORD 'ChangeMe_HR1';
```

Create the Finance role:

```sql id="z1h0qr"
CREATE ROLE finance_role LOGIN PASSWORD 'ChangeMe_FIN1';
```

Create the Audit role:

```sql id="8w5h5m"
CREATE ROLE audit_role LOGIN PASSWORD 'ChangeMe_AUD1';
```

Verify the roles:

```sql id="b6ghj5"
SELECT rolname
FROM pg_roles
WHERE rolname IN (
    'hr_role',
    'finance_role',
    'audit_role'
);
```

Expected:

```text id="qk5c7m"
hr_role
finance_role
audit_role
```

---

# 🧱 Step 5 — Create Employee Records

Create the table:

```sql id="h7v0rq"
CREATE TABLE employee_records (
    emp_id SERIAL PRIMARY KEY,
    full_name TEXT,
    department TEXT,
    salary NUMERIC,
    ssn TEXT,
    audit_flag BOOLEAN DEFAULT false
);
```

Insert sample records:

```sql id="5t6ph4"
INSERT INTO employee_records
(full_name, department, salary, ssn)
VALUES
('Ali Hassan', 'HR', 5000, '123-45-6789'),
('Sara Ahmed', 'Finance', 6000, '987-65-4321'),
('Omar Khalid', 'IT', 5500, '555-55-5555');
```

Verify:

```sql id="l8x3j0"
SELECT * FROM employee_records;
```

---

# 🔒 Step 6 — Configure Column-Level Security

First remove default permissions:

```sql id="iqn7n7"
REVOKE ALL ON employee_records FROM PUBLIC;
```

### 👤 HR

HR receives access to all columns:

```sql id="d1v7cs"
GRANT SELECT ON employee_records TO hr_role;
```

### 💰 Finance

Finance receives only:

```text
emp_id
full_name
department
salary
```

Grant access:

```sql id="v1g5q4"
GRANT SELECT (
    emp_id,
    full_name,
    department,
    salary
)
ON employee_records
TO finance_role;
```

### 📋 Audit

Audit receives only:

```text
emp_id
department
audit_flag
```

Grant access:

```sql id="u4m6qp"
GRANT SELECT (
    emp_id,
    department,
    audit_flag
)
ON employee_records
TO audit_role;
```

---

# 🧱 Step 7 — Enable Row-Level Security

Enable RLS:

```sql id="j7xk4r"
ALTER TABLE employee_records
ENABLE ROW LEVEL SECURITY;
```

---

# 💰 Step 8 — Create Finance RLS Policy

Finance should only see Finance department records.

```sql id="b1v2mq"
CREATE POLICY finance_dept_policy
ON employee_records
FOR SELECT
TO finance_role
USING (department = 'Finance');
```

This means:

```text
Finance Role
     │
     ▼
employee_records
     │
     ▼
department = Finance
     │
     ▼
Only Finance Rows
```

---

# 👤 Step 9 — Create HR RLS Policy

HR can view all employee rows:

```sql id="x1n3z8"
CREATE POLICY hr_all_rows_policy
ON employee_records
FOR SELECT
TO hr_role
USING (true);
```

---

# 📋 Step 10 — Create Audit RLS Policy

Audit should only see records where the audit flag is enabled:

```sql id="w9q3r1"
CREATE POLICY audit_flag_policy
ON employee_records
FOR SELECT
TO audit_role
USING (audit_flag = true);
```

---

# 🔎 Step 11 — Verify RLS Policies

Run:

```sql id="k4y7tz"
SELECT *
FROM pg_policies
WHERE tablename = 'employee_records';
```

You should see the policies for:

```text
finance_role
hr_role
audit_role
```

---

# 📋 Step 12 — Enable pgAudit

Find PostgreSQL configuration:

```bash id="q3b6px"
sudo find / -name "postgresql.conf" 2>/dev/null
```

Open the appropriate configuration file:

```bash id="m8k7xz"
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Add or update:

```text id="g3x1md"
shared_preload_libraries = 'pgaudit'
pgaudit.log = 'read, write, role'
pgaudit.log_relation = on
```

Save the configuration.

---

# 🔄 Step 13 — Restart PostgreSQL

Restart the service:

```bash id="v0w2zq"
sudo systemctl restart postgresql
```

Verify:

```bash id="n2z9qy"
sudo systemctl status postgresql
```

---

# 🔌 Step 14 — Enable pgAudit Extension

Connect to the database:

```bash id="r9z7vw"
sudo -u postgres psql -d agency_records
```

Create the extension:

```sql id="r5m1f7"
CREATE EXTENSION IF NOT EXISTS pgaudit;
```

Verify:

```sql id="q1f8mz"
SELECT *
FROM pg_extension
WHERE extname = 'pgaudit';
```

---

# 📝 Step 15 — Locate PostgreSQL Audit Logs

Find PostgreSQL logs:

```bash id="f7h2cd"
sudo find /var/log/postgresql/ -name "*.log"
```

Monitor the log:

```bash id="a8g4zv"
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

Search for role activity:

```bash id="q5y8rs"
sudo grep "audit_role\|finance_role" \
/var/log/postgresql/postgresql-15-main.log
```

---

# 🧪 Step 16 — Test Finance Access

Connect as Finance:

```bash id="h5c8kw"
psql -U finance_role \
-d agency_records \
-h localhost
```

Run:

```sql id="x7d3qk"
SELECT
    emp_id,
    full_name,
    department,
    salary
FROM employee_records;
```

Expected:

```text
Allowed ✅
```

Finance should see only Finance department rows.

---

## 🚫 Test Restricted SSN

Run:

```sql id="r7x1pm"
SELECT ssn
FROM employee_records;
```

Expected:

```text
Denied ❌
```

---

## 🔐 Test Row-Level Restriction

Run:

```sql id="z8q4mw"
SELECT *
FROM employee_records
WHERE department = 'HR';
```

Expected:

```text
No HR rows returned 🚫
```

---

# 📋 Step 17 — Test Audit Role

Connect:

```bash id="c5v7wn"
psql -U audit_role \
-d agency_records \
-h localhost
```

Test allowed columns:

```sql id="x9j4qk"
SELECT
    emp_id,
    department,
    audit_flag
FROM employee_records;
```

Expected:

```text
Allowed ✅
```

Test restricted salary:

```sql id="h8q2ny"
SELECT salary
FROM employee_records;
```

Expected:

```text
Denied ❌
```

The audit role should only see rows matching:

```text
audit_flag = true
```

---

# 👤 Step 18 — Test HR Role

Connect:

```bash id="k6v8ds"
psql -U hr_role \
-d agency_records \
-h localhost
```

Run:

```sql id="x3z6py"
SELECT *
FROM employee_records;
```

Expected:

```text
Allowed ✅
```

HR should have access to all columns and all employee rows according to the configured policy.

---

# 📊 Step 19 — Access Validation Matrix

Document the results:

| 👤 Role    | 🔎 Query                 | 🎯 Expected Result |
| ---------- | ------------------------ | ------------------ |
| 💰 Finance | `SELECT salary`          | 🚫 Denied          |
| 💰 Finance | Finance employee records | ✅ Allowed          |
| 💰 Finance | HR employee records      | 🚫 Restricted      |
| 📋 Audit   | `SELECT salary`          | 🚫 Denied          |
| 📋 Audit   | Audit columns            | ✅ Allowed          |
| 👤 HR      | `SELECT *`               | ✅ Allowed          |
| 👤 HR      | All departments          | ✅ Allowed          |

---

# 🔍 Step 20 — Verify pgAudit Activity

Search logs:

```bash id="g6v2jk"
sudo grep "audit_role\|finance_role\|hr_role" \
/var/log/postgresql/postgresql-15-main.log
```

Look for evidence of:

* 🔎 SELECT operations
* ✍️ Write operations
* 👥 Role activity
* 🚫 Access attempts
* 📊 Relation-level activity

---

# ⚖️ Step 21 — Document PDPL Alignment

Create the documentation file:

```bash id="q1s7yt"
nano access_model_pdpl.md
```

Include:

```markdown id="h9d4sf"
# Access Model Documentation

## Roles and Justification

### hr_role
Access based on HR responsibilities.

### finance_role
Limited to finance-related employee information.

### audit_role
Limited to audit-related information.

## Controls Implemented

- Column-level restrictions
- Row-level security
- Least-privilege access
- Role separation
- pgAudit logging

## PDPL Alignment

### Data Minimization
Roles receive only the information required for their functions.

### Purpose Limitation
Access is restricted according to the legitimate business purpose of each role.

### Accountability
pgAudit provides records of database access and activity.

### Data Sharing
RBAC reduces the possibility of unauthorized disclosure between departments or agencies.
```

---

# 🛡️ Access Control Model

```text
                  🗄️ Employee Data
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          👤 HR       💰 Finance   📋 Audit
             │           │           │
             ▼           ▼           ▼
         Full Data   Limited Data  Audit Data
             │           │           │
             └───────────┼───────────┘
                         │
                         ▼
                    📋 pgAudit
                         │
                         ▼
                  🔍 Accountability
```

---

# 🔎 Step 22 — Verification

### 1️⃣ Verify Roles

```sql id="s8k2jq"
SELECT rolname
FROM pg_roles
WHERE rolname IN (
    'hr_role',
    'finance_role',
    'audit_role'
);
```

Expected:

```text
hr_role
finance_role
audit_role
```

---

### 2️⃣ Verify RLS

```sql id="c4x8mp"
SELECT relrowsecurity
FROM pg_class
WHERE relname = 'employee_records';
```

Expected:

```text
t
```

---

### 3️⃣ Verify Policies

```sql id="j9r3qf"
SELECT policyname
FROM pg_policies
WHERE tablename = 'employee_records';
```

---

### 4️⃣ Verify pgAudit

```sql id="v5m7ns"
SELECT *
FROM pg_extension
WHERE extname = 'pgaudit';
```

---

### 5️⃣ Verify Logs

```bash id="x4k6yr"
sudo grep "finance_role\|audit_role\|hr_role" \
/var/log/postgresql/postgresql-15-main.log
```

---

### 6️⃣ Verify Documentation

```bash id="h7p2kc"
test -f access_model_pdpl.md && \
echo "Documentation: OK" || \
echo "Documentation: MISSING"
```

---

# 🛠️ Troubleshooting

## ❌ pgAudit Fails to Load

Check:

```text
shared_preload_libraries = 'pgaudit'
```

Confirm the installed PostgreSQL/pgAudit versions match.

Restart PostgreSQL after configuration changes:

```bash id="v8y2wd"
sudo systemctl restart postgresql
```

---

## ❌ Role Login Fails

Check PostgreSQL authentication configuration:

```bash id="p2n4kv"
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Ensure local password authentication is configured appropriately, such as:

```text
scram-sha-256
```

or:

```text
md5
```

---

## ❌ RLS Does Not Restrict Rows

Verify:

```sql id="y5z7xm"
ALTER TABLE employee_records
ENABLE ROW LEVEL SECURITY;
```

Check that the role does not have `BYPASSRLS` privileges.

---

# 🔐 Security Principles Demonstrated

| 🛡️ Principle         | 🔧 Implementation                          |
| --------------------- | ------------------------------------------ |
| Least Privilege       | Roles receive only required permissions    |
| Need-to-Know          | Access is limited to business requirements |
| RBAC                  | Separate HR, Finance, and Audit roles      |
| Column Security       | Sensitive columns restricted               |
| RLS                   | Rows restricted by department or flag      |
| Segregation of Duties | Separate responsibilities                  |
| Accountability        | pgAudit records database activity          |
| Data Minimization     | Unnecessary data is not exposed            |
| Purpose Limitation    | Access follows job function                |
| Monitoring            | Database access is logged                  |

---

# 📊 Skills Demonstrated

![RBAC](https://img.shields.io/badge/RBAC-Access_Control-6A1B9A?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)
![pgAudit](https://img.shields.io/badge/pgAudit-Database_Auditing-336791?style=for-the-badge)
![RLS](https://img.shields.io/badge/RLS-Row_Level_Security-8B0000?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-Security_Controls-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-System_Administration-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![PDPL](https://img.shields.io/badge/PDPL-Privacy_Compliance-00897B?style=for-the-badge)

---

# 🎓 Learning Outcomes

After completing this lab, you should be able to:

* ✅ Create PostgreSQL security roles.
* ✅ Apply least-privilege permissions.
* ✅ Configure column-level security.
* ✅ Configure Row-Level Security.
* ✅ Create role-specific access policies.
* ✅ Configure pgAudit.
* ✅ Monitor database access.
* ✅ Test segregation of duties.
* ✅ Document a privacy-aware access model.
* ✅ Connect technical access controls with PDPL principles.

---

# 🏆 Final Workflow

```text
👥 CREATE ROLES
      ↓
🔒 GRANT MINIMUM PERMISSIONS
      ↓
🧱 ENABLE RLS
      ↓
📋 CONFIGURE pgAudit
      ↓
🧪 TEST EACH ROLE
      ↓
🔍 REVIEW AUDIT LOGS
      ↓
⚖️ MAP CONTROLS TO PDPL
      ↓
✅ VALIDATE NEED-TO-KNOW
```

---

## 👨‍💻 Author

**Hafiz Muhammad Salman**

☁️ Cloud DevOps Engineer | 🐧 Linux Administrator

---

## ⭐ Conclusion

This hands-on lab demonstrates how PostgreSQL can enforce a **need-to-know security model** using RBAC, column-level permissions, Row-Level Security, and pgAudit.

The completed implementation combines:

> **👥 RBAC + 🔒 Least Privilege + 🧱 RLS + 📋 pgAudit + ⚖️ PDPL Alignment**

These controls provide practical experience in designing secure database access for regulated environments where **data minimization, segregation of duties, accountability, and controlled information sharing** are essential.

**🔐 Least Privilege • 🛡️ Need-to-Know • 📋 Accountability • ⚖️ Privacy • 🚀 Secure Systems**
