# 🔐 Logging and Audit Trail for Accountability

<p align="center">
  <img src="https://img.shields.io/badge/GDPR-Art.%205(2)-0052CC?style=for-the-badge&logo=gdpr&logoColor=white" alt="GDPR">
  <img src="https://img.shields.io/badge/GCC-PDPL-6A1B9A?style=for-the-badge" alt="GCC PDPL">
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/auditd-Auditing-4A4A4A?style=for-the-badge" alt="auditd">
  <img src="https://img.shields.io/badge/rsyslog-Logging-CC2927?style=for-the-badge" alt="rsyslog">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Loki-Log%20Aggregation-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Loki">
  <img src="https://img.shields.io/badge/Promtail-Log%20Shipping-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Promtail">
  <img src="https://img.shields.io/badge/Grafana-Visualization-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/SHA--256-Tamper%20Evidence-2E8B57?style=for-the-badge" alt="SHA-256">
  <img src="https://img.shields.io/badge/GNU%20Cron-Scheduling-000000?style=for-the-badge&logo=linux&logoColor=white" alt="Cron">
</p>

---

## 📌 Project Overview

This hands-on lab implements an **end-to-end logging and accountability pipeline** on a single Linux machine.

The lab captures access activity using `auditd` and `rsyslog`, forwards logs to a local **Grafana Loki** instance using **Promtail**, creates hourly SHA-256 hashes to provide tamper-evidence, visualizes events through **Grafana**, and packages audit artifacts into an evidence pack.

### 🔄 End-to-End Architecture

```text
                         ┌─────────────────────────┐
                         │      Linux System       │
                         │                         │
                         │  customers.csv          │
                         │  Database/App Activity  │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  ┌──────────────┐         ┌──────────────┐
                  │    auditd    │         │    rsyslog   │
                  │ System Audit │         │ App/DB Logs  │
                  └───────┬──────┘         └──────┬───────┘
                          │                       │
                          └───────────┬───────────┘
                                      ▼
                              ┌──────────────┐
                              │   Log Files  │
                              └───────┬──────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │   Promtail   │
                              │ Log Shipper  │
                              └───────┬──────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │     Loki     │
                              │ Log Storage  │
                              └───────┬──────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │   Grafana    │
                              │ Visualization│
                              └──────────────┘

               ┌──────────────────────────────┐
               │     SHA-256 Hash Ledger      │
               │      Tamper Evidence         │
               └──────────────┬───────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Evidence Pack  │
                     │ Audit Artifacts │
                     └─────────────────┘
```

---

# 🎯 Objectives

By completing this lab, you will be able to:

* 🔍 Configure `auditd` for system access auditing
* 📝 Configure `rsyslog` for application/database access logging
* 📡 Forward logs to a local Loki instance
* 🚚 Use Promtail as a log shipping agent
* 🔐 Generate SHA-256 hashes of log files
* 🛡️ Detect modifications through hash comparison
* 📊 Visualize access events in Grafana
* 📋 Create a structured compliance evidence pack
* 🔎 Query audit events using `ausearch`
* 🧾 Demonstrate accountability controls for privacy compliance
* 🏛️ Relate technical controls to GDPR Article 5(2) and GCC PDPL accountability principles

---

# 🧰 Technology Stack

| Technology      | Purpose                                  |
| --------------- | ---------------------------------------- |
| 🐧 Ubuntu Linux | Lab operating system                     |
| 🔐 auditd       | System-level audit logging               |
| 📝 rsyslog      | Application/system log collection        |
| 📡 Promtail     | Log shipping                             |
| 📦 Loki         | Centralized log storage                  |
| 📊 Grafana      | Log visualization                        |
| 🔑 SHA-256      | Log integrity/tamper evidence            |
| ⏰ Cron          | Hourly hash scheduling                   |
| 🐚 Bash         | Automation scripts                       |
| 🗃️ SQLite      | Sample database tooling                  |
| 🔎 ausearch     | Audit event searching                    |
| 📦 tar          | Evidence package creation                |
| 🛡️ GDPR        | Privacy accountability framework         |
| 🏛️ GCC PDPL    | Data protection accountability framework |

---

# 📋 Prerequisites

Before starting, you should have:

* Basic Linux command-line knowledge
* Familiarity with `systemctl`
* Basic understanding of Linux permissions
* Basic knowledge of cron
* Basic SQL/database familiarity
* Basic understanding of GDPR/PDPL accountability principles
* A Linux VM with `sudo` privileges

### 🖥️ Recommended Environment

```text
OS: Ubuntu 22.04+
RAM: 4 GB+
CPU: 2 cores+
Privileges: sudo
Network: Internet required for initial package downloads
Cloud Account: Not required
```

---

# 🏗️ Environment Setup

## 🚀 Step 1 — Update the System

```bash
sudo apt update
```

Upgrade packages if required:

```bash
sudo apt upgrade -y
```

### ✨ Technology

![Ubuntu](https://img.shields.io/badge/Ubuntu-Linux-E95420?style=flat-square\&logo=ubuntu\&logoColor=white)

---

## 📦 Step 2 — Install Required Packages

```bash
sudo apt install -y \
  auditd \
  audispd-plugins \
  rsyslog \
  sqlite3 \
  curl \
  unzip \
  gnupg
```

Verify:

```bash
auditctl -v
rsyslogd -v
sqlite3 --version
gpg --version
```

### ✨ Technology

![auditd](https://img.shields.io/badge/auditd-Audit%20Framework-4A4A4A?style=flat-square)
![rsyslog](https://img.shields.io/badge/rsyslog-Logging-CC2927?style=flat-square)

---

# 📦 Loki and Promtail Installation

## 🔶 Step 3 — Download Loki

```bash
curl -O -L \
"https://github.com/grafana/loki/releases/latest/download/loki-linux-amd64.zip"
```

Extract:

```bash
unzip loki-linux-amd64.zip
```

Move:

```bash
sudo mv loki-linux-amd64 /usr/local/bin/loki
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/loki
```

Verify:

```bash
loki --version
```

### ✨ Technology

![Loki](https://img.shields.io/badge/Grafana-Loki-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

## 📡 Step 4 — Install Promtail

Download:

```bash
curl -O -L \
"https://github.com/grafana/loki/releases/latest/download/promtail-linux-amd64.zip"
```

Extract:

```bash
unzip promtail-linux-amd64.zip
```

Move:

```bash
sudo mv promtail-linux-amd64 /usr/local/bin/promtail
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/promtail
```

Verify:

```bash
promtail --version
```

### ✨ Technology

![Promtail](https://img.shields.io/badge/Promtail-Log%20Shipper-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

# 📊 Grafana Installation

## 🔶 Step 5 — Install Grafana Repository

```bash
sudo apt install -y software-properties-common wget
```

Add the Grafana signing key:

```bash
wget -q -O - \
https://apt.grafana.com/gpg.key | \
sudo gpg --dearmor \
-o /usr/share/keyrings/grafana.gpg
```

Add the repository:

```bash
echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://apt.grafana.com stable main" | \
sudo tee /etc/apt/sources.list.d/grafana.list
```

Update:

```bash
sudo apt update
```

Install Grafana:

```bash
sudo apt install -y grafana
```

Verify:

```bash
grafana-server -v
```

### ✨ Technology

![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

# 🔐 Task 1 — Configure auditd and rsyslog

## 🎯 Objective

Capture access events against a sample file representing sensitive customer information.

---

## 📁 Step 1 — Create Sample Application Data

Create the directory:

```bash
sudo mkdir -p /var/lib/appdata
```

Create the sample data file:

```bash
echo "id,name,email" | \
sudo tee /var/lib/appdata/customers.csv
```

Verify:

```bash
sudo cat /var/lib/appdata/customers.csv
```

Expected:

```text
id,name,email
```

---

## 🔍 Step 2 — Add an auditd Watch Rule

```bash
sudo auditctl \
-w /var/lib/appdata/customers.csv \
-p rwa \
-k pdpl_access
```

### Rule Meaning

| Option | Meaning                |
| ------ | ---------------------- |
| `-w`   | Watch a file           |
| `-p`   | Permissions to monitor |
| `r`    | Read                   |
| `w`    | Write                  |
| `a`    | Attribute changes      |
| `-k`   | Searchable audit key   |

The audit key is:

```text
pdpl_access
```

---

## 💾 Step 3 — Persist the Rule

```bash
echo "-w /var/lib/appdata/customers.csv -p rwa -k pdpl_access" | \
sudo tee -a /etc/audit/rules.d/audit.rules
```

Restart auditd:

```bash
sudo systemctl restart auditd
```

Verify:

```bash
sudo auditctl -l
```

You should see the `pdpl_access` rule.

### ✨ Technology

![auditd](https://img.shields.io/badge/auditd-System%20Auditing-4A4A4A?style=flat-square)

---

# 📝 Configure Application/Database Access Logging

## 📝 Step 4 — Create the Access Log

```bash
sudo touch /var/log/db_access.log
```

Set suitable ownership/permissions for your lab environment.

For example:

```bash
sudo chmod 640 /var/log/db_access.log
```

---

## 🐚 Step 5 — Create the Simulation Script

Create:

```bash
sudo nano /usr/local/bin/simulate_access.sh
```

Add:

```bash
#!/bin/bash

TIMESTAMP=$(date --iso-8601=seconds)
USER_NAME=$(whoami)

echo "$TIMESTAMP USER=$USER_NAME ACTION=SELECT TABLE=customers" \
  | sudo tee -a /var/log/db_access.log > /dev/null
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/simulate_access.sh
```

Run it:

```bash
sudo /usr/local/bin/simulate_access.sh
```

Run multiple times:

```bash
sudo /usr/local/bin/simulate_access.sh
sudo /usr/local/bin/simulate_access.sh
sudo /usr/local/bin/simulate_access.sh
```

Review:

```bash
sudo cat /var/log/db_access.log
```

Example:

```text
2026-08-17T08:00:01+05:00 USER=salman ACTION=SELECT TABLE=customers
2026-08-17T08:02:14+05:00 USER=salman ACTION=SELECT TABLE=customers
```

### ✨ Technology

![Bash](https://img.shields.io/badge/Bash-Scripting-4EAA25?style=flat-square\&logo=gnu-bash\&logoColor=white)
![rsyslog](https://img.shields.io/badge/rsyslog-Application%20Logging-CC2927?style=flat-square)

---

## 🔎 Step 6 — Query audit Events

```bash
sudo ausearch -k pdpl_access | tail -20
```

This searches for events associated with:

```text
pdpl_access
```

---

# 📡 Task 2 — Forward Logs to Loki

## 🎯 Objective

Centralize application and audit logs using Loki.

### Architecture

```text
/var/log/db_access.log
          │
          ▼
       Promtail
          │
          ▼
         Loki
          │
          ▼
       Grafana
```

---

## ⚙️ Step 1 — Create Loki Configuration

Create:

```bash
nano ~/data-portability-lab/loki-config.yaml
```

Example minimal configuration:

```yaml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /tmp/loki
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h
```

> ⚠️ Loki configuration schemas can change between releases. For production use, validate the configuration against the documentation for the exact Loki version installed.

---

## ▶️ Step 2 — Start Loki

```bash
loki -config.file=loki-config.yaml &
```

Verify:

```bash
curl http://localhost:3100/ready
```

Expected:

```text
ready
```

### ✨ Technology

![Loki](https://img.shields.io/badge/Loki-Centralized%20Logging-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

# 📡 Step 3 — Create Promtail Configuration

Create:

```bash
nano ~/data-portability-lab/promtail-config.yaml
```

Add:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://localhost:3100/loki/api/v1/push

scrape_configs:

  - job_name: db_access

    static_configs:
      - targets:
          - localhost

        labels:
          job: db_access
          __path__: /var/log/db_access.log

  - job_name: audit_log

    static_configs:
      - targets:
          - localhost

        labels:
          job: audit_log
          __path__: /var/log/audit/audit.log
```

### 🔑 Important Path

The audit log should normally be:

```text
/var/log/audit/audit.log
```

---

## ▶️ Step 4 — Start Promtail

```bash
promtail \
-config.file=promtail-config.yaml &
```

Check the process:

```bash
ps aux | grep promtail
```

### ✨ Technology

![Promtail](https://img.shields.io/badge/Promtail-Log%20Collection-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

## 🔎 Step 5 — Query Loki

Query application logs:

```bash
curl -G -s \
"http://localhost:3100/loki/api/v1/query" \
--data-urlencode 'query={job="db_access"}' \
| head -c 300
```

Query audit logs:

```bash
curl -G -s \
"http://localhost:3100/loki/api/v1/query" \
--data-urlencode 'query={job="audit_log"}' \
| head -c 300
```

A successful response indicates Loki is receiving log data.

---

# 🔐 Task 3 — Hourly Log Hashing

## 🎯 Objective

Generate SHA-256 hashes of important log files and maintain a timestamped ledger.

### Integrity Model

```text
Log File
   │
   ▼
SHA-256
   │
   ▼
Hash Digest
   │
   ▼
Tamper-Evidence Ledger
```

---

## 📝 Step 1 — Create Hashing Script

```bash
sudo nano /usr/local/bin/hash_logs.sh
```

Add:

```bash
#!/bin/bash

LOGS=(
  "/var/log/db_access.log"
  "/var/log/audit/audit.log"
)

LEDGER="/var/log/audit_hash_ledger.log"

TIMESTAMP=$(date --iso-8601=seconds)

for f in "${LOGS[@]}"; do

    if [ -f "$f" ]; then

        HASH=$(sha256sum "$f" | awk '{print $1}')

        echo "$TIMESTAMP $f $HASH" \
          | sudo tee -a "$LEDGER" > /dev/null

    fi

done
```

Make executable:

```bash
sudo chmod +x /usr/local/bin/hash_logs.sh
```

---

## ▶️ Step 2 — Test Manually

```bash
sudo /usr/local/bin/hash_logs.sh
```

Inspect:

```bash
sudo cat /var/log/audit_hash_ledger.log
```

Example:

```text
2026-08-17T08:00:00+05:00 /var/log/db_access.log abc123...
2026-08-17T08:00:00+05:00 /var/log/audit/audit.log def456...
```

---

## ⏰ Step 3 — Schedule Hourly Hashing

```bash
(crontab -l 2>/dev/null; \
echo "0 * * * * /usr/local/bin/hash_logs.sh") | crontab -
```

Verify:

```bash
crontab -l
```

Expected:

```text
0 * * * * /usr/local/bin/hash_logs.sh
```

### ✨ Technology

![SHA-256](https://img.shields.io/badge/SHA--256-Tamper%20Evidence-2E8B57?style=flat-square)
![Cron](https://img.shields.io/badge/Cron-Scheduled%20Hashing-000000?style=flat-square\&logo=linux\&logoColor=white)

---

# 🧪 Tamper Detection Test

Modify the database access log:

```bash
echo "TAMPER_TEST" | \
sudo tee -a /var/log/db_access.log
```

Generate a new hash:

```bash
sudo /usr/local/bin/hash_logs.sh
```

Inspect:

```bash
sudo cat /var/log/audit_hash_ledger.log
```

Compare the consecutive hashes for:

```text
/var/log/db_access.log
```

The hash should change after the file modification.

> **Important:** A local hash ledger provides tamper-evidence, not absolute tamper-proof protection. An attacker with sufficient privileges could modify both the log and ledger. Stronger production designs should place integrity records in a separate protected or immutable system.

---

# 📊 Task 4 — Build a Grafana Dashboard

## 🎯 Objective

Create a dashboard that allows security and compliance teams to visualize access activity.

---

## ▶️ Step 1 — Start Grafana

```bash
sudo systemctl start grafana-server
```

Enable at boot:

```bash
sudo systemctl enable grafana-server
```

Check status:

```bash
sudo systemctl status grafana-server
```

Open:

```text
http://<VM-IP>:3000
```

### ✨ Technology

![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=flat-square\&logo=grafana\&logoColor=white)

---

# 🔌 Step 2 — Add Loki Data Source

In Grafana:

```text
Configuration
      ↓
Data Sources
      ↓
Add data source
      ↓
Loki
```

Use:

```text
http://localhost:3100
```

Click:

```text
Save & Test
```

The connection should succeed.

---

# 📋 Step 3 — Create Logs Panel

Create a new dashboard.

Add a **Logs** panel.

Use:

```logql
{job="db_access"}
```

This displays application/database access events.

---

# 📈 Step 4 — Create Audit Event Count Panel

Create a second panel.

A basic LogQL metric query can be:

```logql
count_over_time({job="audit_log"}[5m])
```

This counts audit log entries received during each five-minute interval.

If you want to focus on records associated with the `pdpl_access` audit key and the text is present in the log line, use a filter such as:

```logql
count_over_time({job="audit_log"} |= "pdpl_access"[5m])
```

Save the dashboard as:

```text
PDPL Accountability Dashboard
```

### Dashboard Layout

```text
┌─────────────────────────────────────────────┐
│       PDPL Accountability Dashboard         │
├─────────────────────────────────────────────┤
│                                             │
│       📋 Database Access Logs               │
│       {job="db_access"}                     │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│       📈 Audit Events / 5 Minutes           │
│       count_over_time(...)                  │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 📦 Task 5 — Produce an Evidence Pack

## 🎯 Objective

Collect relevant artifacts into a structured package suitable for review by security, compliance, or audit teams.

---

## 📁 Step 1 — Create Evidence Directory

```bash
mkdir -p ~/evidence_pack
```

---

## 📋 Step 2 — Copy the Hash Ledger

```bash
sudo cp \
/var/log/audit_hash_ledger.log \
~/evidence_pack/
```

---

## 🔎 Step 3 — Export audit Events

```bash
sudo ausearch -k pdpl_access \
> ~/evidence_pack/audit_events.txt
```

---

## 📝 Step 4 — Copy Application Logs

```bash
sudo cp \
/var/log/db_access.log \
~/evidence_pack/
```

---

# 📖 Step 5 — Create Evidence README

```bash
nano ~/evidence_pack/README.md
```

Include:

```markdown
# PDPL Accountability Evidence Pack

## Scope

This evidence pack documents monitoring of access to:

/var/lib/appdata/customers.csv

The sample file represents customer information containing
fields such as ID, name, and email.

## Logging Mechanisms

The environment uses:

- auditd for operating-system file access auditing
- rsyslog/application logging for simulated database access
- Promtail for log shipping
- Loki for centralized log storage
- Grafana for visualization
- SHA-256 for log integrity evidence

## Integrity Verification

The hash ledger contains SHA-256 digests of monitored log files.

To verify integrity:

1. Recalculate the SHA-256 hash.
2. Compare it with the recorded ledger value.
3. Investigate any unexpected difference.

## Compliance Mapping

The controls support accountability objectives associated
with GDPR Article 5(2) and GCC PDPL requirements.

The evidence demonstrates that access activity is logged,
centralized, integrity-checked, visualized, and retained
as an audit artifact.

## Evidence Files

- audit_hash_ledger.log
- audit_events.txt
- db_access.log
```

---

# 📦 Step 6 — Package the Evidence

From your home directory:

```bash
tar -czvf \
evidence_pack_$(date +%F).tar.gz \
-C ~ evidence_pack
```

Generate checksum:

```bash
sha256sum \
evidence_pack_$(date +%F).tar.gz \
> evidence_pack_checksum.txt
```

Verify:

```bash
cat evidence_pack_checksum.txt
```

---

# 🔍 Verification

## ✅ Check 1 — Verify audit Rule

```bash
sudo auditctl -l
```

Confirm the output contains:

```text
pdpl_access
```

---

## ✅ Check 2 — Verify Loki

```bash
curl -G -s \
"http://localhost:3100/loki/api/v1/query" \
--data-urlencode 'query={job="db_access"}' \
| head -c 300
```

Then:

```bash
curl -G -s \
"http://localhost:3100/loki/api/v1/query" \
--data-urlencode 'query={job="audit_log"}' \
| head -c 300
```

---

## ✅ Check 3 — Verify Hash Ledger

```bash
sudo cat /var/log/audit_hash_ledger.log
```

Confirm there are at least two timestamped entries after running the hashing process more than once.

---

## ✅ Check 4 — Verify Grafana

Confirm:

```text
PDPL Accountability Dashboard
```

contains:

* 📋 Database access logs
* 📈 Audit event count

---

## ✅ Check 5 — Verify Evidence Package

```bash
ls -lh evidence_pack_*.tar.gz
```

Verify checksum:

```bash
sha256sum -c evidence_pack_checksum.txt
```

Expected:

```text
OK
```

---

# 🧪 Final Verification Checklist

* [ ] `auditd` installed and running
* [ ] `pdpl_access` audit rule configured
* [ ] Audit rule persisted in `/etc/audit/rules.d/`
* [ ] `db_access.log` created
* [ ] Simulated database events generated
* [ ] `ausearch` returns audit events
* [ ] Loki running on port `3100`
* [ ] Promtail shipping logs
* [ ] `db_access` logs visible in Loki
* [ ] `audit_log` logs visible in Loki
* [ ] SHA-256 hashing script created
* [ ] Hash ledger contains multiple entries
* [ ] Cron job configured for hourly execution
* [ ] Tamper test successfully detects a change
* [ ] Grafana connected to Loki
* [ ] PDPL Accountability Dashboard created
* [ ] Evidence pack created
* [ ] Evidence archive checksum generated
* [ ] Checksum verification succeeds

---

# 🛠️ Troubleshooting

## ❌ Promtail Is Not Shipping Logs

Check Promtail:

```bash
ps aux | grep promtail
```

Check its output/errors.

Verify log permissions:

```bash
sudo ls -l /var/log/db_access.log
sudo ls -l /var/log/audit/audit.log
```

Check the Promtail positions file:

```bash
cat /tmp/positions.yaml
```

Make sure the configured paths exist.

---

## ❌ auditd Rule Disappeared

Check:

```bash
sudo auditctl -l
```

Verify the persistent rule:

```bash
sudo cat /etc/audit/rules.d/audit.rules
```

Confirm:

```text
-w /var/lib/appdata/customers.csv -p rwa -k pdpl_access
```

---

## ❌ Grafana Cannot Connect to Loki

Check Loki:

```bash
curl http://localhost:3100/ready
```

Check the listening port:

```bash
sudo ss -lntp | grep 3100
```

Confirm Grafana's Loki URL is:

```text
http://localhost:3100
```

---

## ❌ No Audit Events

Generate an access:

```bash
sudo cat /var/lib/appdata/customers.csv
```

Then search:

```bash
sudo ausearch -k pdpl_access
```

---

## ❌ Hash Does Not Change

Make sure the log was actually modified:

```bash
sudo tail /var/log/db_access.log
```

Then run:

```bash
sudo /usr/local/bin/hash_logs.sh
```

Compare the latest hash entries.

---

# 🔐 Security Considerations

This lab demonstrates several important security principles:

### 🛡️ Accountability

Actions against sensitive data are recorded and can be reviewed.

### 🔍 Traceability

Audit events contain information that can help determine who accessed monitored resources and when.

### 🔐 Integrity

SHA-256 provides evidence that a file's contents changed when the digest changes.

### 📡 Centralization

Loki provides a centralized location for collected log data.

### 📊 Visibility

Grafana makes access activity easier for security and compliance teams to review.

### 📦 Evidence Preservation

The evidence pack collects relevant artifacts into a reproducible audit package.

---

# 🏛️ Compliance Mapping

| Accountability Concept     | Technical Control                 |
| -------------------------- | --------------------------------- |
| 📋 Demonstrable compliance | Evidence pack                     |
| 🔍 Access accountability   | `auditd`                          |
| 📝 Application logging     | `rsyslog` / application log       |
| 🔐 Integrity evidence      | SHA-256 hashes                    |
| 📡 Centralized monitoring  | Loki                              |
| 📊 Monitoring/visibility   | Grafana                           |
| 📦 Audit evidence          | TAR archive + checksum            |
| 🇪🇺 GDPR Art. 5(2)        | Accountability evidence           |
| 🌍 GCC PDPL                | Technical accountability controls |

> ⚠️ This lab provides a technical demonstration of accountability controls. Actual GDPR or GCC PDPL compliance requires organizational, legal, governance, retention, access-control, and other controls beyond this lab.

---

# 📂 Project Structure

After completing the lab:

```text
logging-audit-trail/
│
├── loki-config.yaml
├── promtail-config.yaml
│
├── simulate_access.sh
├── hash_logs.sh
│
├── evidence_pack/
│   ├── README.md
│   ├── audit_events.txt
│   ├── audit_hash_ledger.log
│   └── db_access.log
│
├── evidence_pack_YYYY-MM-DD.tar.gz
└── evidence_pack_checksum.txt
```

---

# 🧠 Skills Demonstrated

```text
🐧 Linux System Administration
🔐 Linux Auditing
📝 Log Management
📡 Log Shipping
📦 Centralized Logging
📊 Observability
🔎 Security Monitoring
🔑 Cryptographic Hashing
⏰ Cron Automation
🐚 Bash Scripting
📋 Compliance Evidence Collection
🛡️ Privacy Accountability
🇪🇺 GDPR Awareness
🌍 GCC PDPL Awareness
📈 Grafana Dashboard Development
```

---

# 🚀 Real-World Applications

The techniques demonstrated in this lab are applicable to:

* Security Operations Centers (SOC)
* Security Engineering
* Compliance Engineering
* Privacy Engineering
* Linux Administration
* Audit and Governance
* Incident Response
* Access Monitoring
* Data Protection Programs
* ISO 27001-aligned environments
* GDPR accountability programs
* GCC PDPL-oriented control environments

---

# 🌟 Conclusion

This lab built an end-to-end **Logging and Audit Trail for Accountability** pipeline on a Linux host.

The workflow captures access events using **auditd and application logging**, ships events through **Promtail**, stores them in **Grafana Loki**, visualizes them using **Grafana**, creates **SHA-256 tamper-evidence records**, and packages the resulting artifacts into a structured evidence pack.

The complete workflow can be summarized as:

```text
       ACCESS EVENT
            │
            ▼
      ┌───────────┐
      │  auditd   │
      └─────┬─────┘
            │
            ▼
       Audit Logs
            │
            ▼
      ┌───────────┐
      │ Promtail  │
      └─────┬─────┘
            │
            ▼
      ┌───────────┐
      │   Loki    │
      └─────┬─────┘
            │
            ▼
      ┌───────────┐
      │  Grafana  │
      └───────────┘

            +
            
      ┌───────────┐
      │ SHA-256   │
      │ Hashing   │
      └─────┬─────┘
            │
            ▼
      Evidence Ledger
            │
            ▼
      Compliance Pack
```

### 🎯 Final Outcome

**Capture → Centralize → Protect → Visualize → Verify → Preserve**

This provides a practical foundation for demonstrating technical accountability and supporting security/compliance audit activities.

---

<p align="center">

## 🔐 Log Everything • Protect Integrity • Prove Accountability

</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Audit-auditd-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Logs-Loki-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Visualization-Grafana-F46800?style=for-the-badge">
  <img src="https://img.shields.io/badge/Integrity-SHA--256-green?style=for-the-badge">
</p>
