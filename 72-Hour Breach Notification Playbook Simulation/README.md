
<div align="center">

# 🚨 72-Hour Breach Notification Playbook Simulation

![Wazuh](https://img.shields.io/badge/Wazuh-3AB7C3?style=for-the-badge&logo=wazuh&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-003399?style=for-the-badge&logo=europeanunion&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

*Detect a simulated PII breach with Wazuh, classify it, and draft regulator/data-subject notifications inside a 72-hour clock*

</div>

---

## 📖 Table of Contents

- [🎯 Objectives](#-objectives)
- [📋 Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [🕵️ Task 1: Stage the Mock Breach and Configure Detection](#️-task-1-stage-the-mock-breach-and-configure-detection)
- [🔔 Task 2: Trigger and Validate Alerts](#-task-2-trigger-and-validate-alerts)
- [⚖️ Task 3: Classify Severity and Affected Data Subjects](#️-task-3-classify-severity-and-affected-data-subjects)
- [📨 Task 4: Draft Notifications Within the 72-Hour Window](#-task-4-draft-notifications-within-the-72-hour-window)
- [🗂️ Task 5: Tabletop Review and Lessons Learned](#️-task-5-tabletop-review-and-lessons-learned)
- [✅ Verification](#-verification)
- [🎯 MITRE ATT&CK Mapping](#-mitre-attck-mapping)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Objectives

| # | By completing this lab, you will... |
|---|---|
| 1 | Deploy and configure Wazuh SIEM to detect indicators of a personal data breach |
| 2 | Build detection rules that trigger on sensitive data exposure patterns in web application logs |
| 3 | Apply GDPR Article 33/34 and GCC PDPL-equivalent criteria to classify breach severity and notification obligations |
| 4 | Produce regulator-ready and data-subject-ready breach notifications within a simulated 72-hour window |
| 5 | Conduct a structured tabletop review and document lessons learned using an IR after-action framework |

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| Linux system administration | Strong understanding of log formats and syslog/JSON pipelines |
| SIEM architecture | Working knowledge — agents, indexers, rule engines |
| GDPR knowledge | Familiarity with Articles 33/34 and general regional PDPL breach notification duties |
| Scripting | Basic Bash/Python for log generation and parsing |
| Docker | Comfortable with Docker or native package installation on Linux |

## 🖥️ Lab Environment

> A single Linux machine (Ubuntu 22.04 LTS) is provided via Al Nafi **Start Lab**. Minimum 4 vCPU / 8GB RAM recommended for a Wazuh single-node install. Internet access is required for package repositories.

```bash
# ✅ Verify base environment
lsb_release -a
free -h
docker --version || sudo apt install -y docker.io docker-compose-plugin
```

Install Wazuh (single-node, Docker-based — avoids managed cloud dependency):

```bash
# 🐳 Deploy Wazuh single-node via Docker
git clone https://github.com/wazuh/wazuh-docker.git -b v4.9.0
cd wazuh-docker/single-node
docker compose up -d
# Access dashboard at https://<lab-ip>:443 (default admin creds in docs/README)
```

Set up a mock vulnerable web app to generate breach-like logs (e.g., a simple Flask app or `python3 -m http.server` with a custom access-log wrapper). Architecture:

```
[Mock Web App] --> [access.log] --> [Wazuh Agent] --> [Wazuh Manager] --> [Alerts/Dashboard]
```

---

## 🕵️ Task 1: Stage the Mock Breach and Configure Detection

Design a mock web application log (Apache/Flask combined log format) containing:
- Simulated unauthorized access to an endpoint like `/export/customers.csv`
- Records including PII fields (name, email, national ID pattern) exfiltrated in bulk (e.g., >500 records in one request/session)

Install the Wazuh agent on the same host and register it to the manager; point it to the mock app's log path via the `ossec.conf` `<localfile>` block.

Write a custom Wazuh decoder and rule (XML, in `/var/ossec/etc/rules/local_rules.xml`) that:
- Detects bulk data export patterns (high-volume GET/POST to sensitive endpoints)
- Flags PII-pattern regex matches (e.g., email or national ID regex) in response payloads or query strings
- Assigns a custom rule level (severity) consistent with a data breach indicator

```xml
<!-- local_rules.xml : skeleton only -->
<group name="local,data_breach,">
  <rule id="100100" level="TODO">
    <if_sid>TODO_base_web_rule_id</if_sid>
    <match>TODO_regex_or_pattern</match>
    <description>TODO description of breach indicator</description>
    <group>pii_exposure,</group>
  </rule>
  <!-- Add a correlated rule for volume/frequency-based detection -->
</group>
```

Generate the mock breach traffic using a script you write (Python or Bash) that floods the endpoint with requests containing fake PII.

> 📦 **Deliverable:** Working decoder/rule set + a log-replay script that reliably triggers your rule.

---

## 🔔 Task 2: Trigger and Validate Alerts

- Restart the Wazuh manager and agent services; confirm rule syntax with `/var/ossec/bin/wazuh-logtest`
- Replay your mock breach script against the log source
- Validate alert generation in the Wazuh dashboard (Security Events) and via API/CLI (`/var/ossec/logs/alerts/alerts.json`)
- Extract and timestamp the alert to establish your "detection time" — this is **T0** for the 72-hour clock

```bash
# 🧪 Test your rule logic before deployment
sudo /var/ossec/bin/wazuh-logtest

# 📡 Tail raw alerts to confirm firing
tail -f /var/ossec/logs/alerts/alerts.json | jq 'select(.rule.id=="100100")'
```

> 📦 **Deliverable:** Screenshot/export of the triggered alert with timestamp; a short note identifying T0.

---

## ⚖️ Task 3: Classify Severity and Affected Data Subjects

Using the alert data, write a Python or Bash parsing script that extracts from `alerts.json`:
- Number of unique data subjects affected (deduplicate by PII identifier)
- Categories of data exposed (identify special category data per GDPR Art. 9 if present)
- Attack vector and exposure duration (first-seen to last-seen timestamps)

Apply a risk classification framework (you determine the criteria, justify with reference to GDPR Art. 33(1) "risk to rights and freedoms" test and DPIA-style scoring) to decide:
- Is supervisory authority notification required? (Y/N + justification)
- Is data subject notification required under Art. 34 / high-risk threshold? (Y/N + justification)

```python
def analyze_breach_alerts(alerts_path: str) -> dict:
    """
    Parse Wazuh alerts.json and produce a breach impact summary.

    Args:
        alerts_path: path to alerts.json

    Returns:
        dict with keys: affected_subjects_count, data_categories,
        first_seen, last_seen, risk_score, notification_required (bool)
    """
    # TODO: parse JSONL alerts file
    # TODO: deduplicate affected subjects
    # TODO: classify data categories (regular vs special category)
    # TODO: compute a risk score against your own defined rubric
    # TODO: return structured summary
    pass
```

> 📦 **Deliverable:** Risk classification report (markdown or JSON) with justification mapped to GDPR Art. 33(1)/34(1) criteria and equivalent GCC PDPL articles (e.g., UAE PDPL, Saudi PDPL) you research independently.

---

## 📨 Task 4: Draft Notifications Within the 72-Hour Window

Using your Task 3 output, draft two notification documents:
- **Supervisory Authority Notification** — must include (per Art. 33(3)): nature of breach, categories/approx. number of subjects and records, DPO contact, likely consequences, mitigation measures taken/proposed
- **Data Subject Notification** (if triggered) — plain-language equivalent per Art. 34(2)

Calculate and clearly state the notification deadline (T0 + 72 hours) and whether your simulated response met it.

Store both documents as Markdown files in a `notifications/` directory on the lab machine.

> 📦 **Deliverable:** Two notification drafts + a deadline compliance statement (met/missed, with reasoning).

---

## 🗂️ Task 5: Tabletop Review and Lessons Learned

- Conduct a self-run tabletop exercise: document a timeline (detection, triage, classification, notification decision, drafting) with actual timestamps from your simulation
- Identify at least three process gaps or detection blind spots (e.g., delayed alert triage, missing data classification tagging, incomplete Wazuh rule coverage)
- Produce an After-Action Report covering: what worked, what failed, remediation actions, and updated playbook recommendations

> 📦 **Deliverable:** `after_action_report.md` with timeline table, gap analysis, and remediation plan.

---

## ✅ Verification

Confirm on the lab machine:

```bash
# 1️⃣ Wazuh services running
sudo systemctl status wazuh-manager wazuh-agent

# 2️⃣ Custom rule loaded without errors
sudo /var/ossec/bin/wazuh-logtest -c /var/ossec/etc/rules/local_rules.xml

# 3️⃣ Alert exists for the mock breach
jq 'select(.rule.id=="100100")' /var/ossec/logs/alerts/alerts.json | head

# 4️⃣ Deliverables present
ls -la notifications/ after_action_report.md breach_analysis_output.*
```

- [ ] Alert timestamp (T0) correctly referenced in both notification drafts
- [ ] Notification deadline math verifiable (T0 + 72h shown explicitly)
- [ ] After-action report contains timeline table and minimum 3 identified gaps

---

## 🎯 MITRE ATT&CK Mapping

| Technique ID | Technique | Relevance |
|---|---|---|
| T1190 | Exploit Public-Facing Application | Unauthorized bulk access to the `/export/customers.csv` endpoint |
| T1213 | Data from Information Repositories | Bulk exfiltration of customer PII records from the application |
| T1005 | Data from Local System | Reading and staging sensitive data files ahead of exfiltration |
| T1567 | Exfiltration Over Web Service | High-volume data transfer out via the exposed web endpoint |

---

## 🏁 Conclusion

### 🎉 Key Accomplishments
- Built an end-to-end breach detection and response simulation on a single Linux host using Wazuh SIEM
- Engineered custom detection rules to identify PII exposure patterns and validated alerting
- Applied regulatory risk criteria from GDPR and GCC PDPL frameworks to classify breach severity
- Produced real-world-style notification documents for both supervisory authorities and data subjects within a simulated 72-hour compliance window
- Closed the exercise with a tabletop review generating actionable lessons learned

### 💼 Real-World Applications
This workflow mirrors the responsibilities of an **Incident Response Analyst** and **DPO** operating under **GDPR Art. 33/34** and equivalent regional breach notification law.

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Education-blue?style=for-the-badge)

</div>
