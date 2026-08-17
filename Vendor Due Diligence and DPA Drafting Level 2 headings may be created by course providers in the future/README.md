# 🔐 Vendor Due Diligence and DPA Drafting

<p align="center">
  <img src="https://img.shields.io/badge/Vendor-Risk%20Management-0052CC?style=for-the-badge" alt="Vendor Risk Management">
  <img src="https://img.shields.io/badge/GDPR-Article%2028-0A66C2?style=for-the-badge" alt="GDPR">
  <img src="https://img.shields.io/badge/UAE-PDPL-6A1B9A?style=for-the-badge" alt="UAE PDPL">
  <img src="https://img.shields.io/badge/KSA-PDPL-006C35?style=for-the-badge" alt="KSA PDPL">
  <img src="https://img.shields.io/badge/Linux-Bash-E95420?style=for-the-badge&logo=linux&logoColor=white" alt="Linux">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CSV-Data%20Analysis-217346?style=for-the-badge" alt="CSV">
  <img src="https://img.shields.io/badge/JSON-Baseline-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON">
  <img src="https://img.shields.io/badge/Markdown-Documentation-000000?style=for-the-badge&logo=markdown&logoColor=white" alt="Markdown">
  <img src="https://img.shields.io/badge/Virtualenv-Python%20Environment-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Virtualenv">
</p>

---

## 📌 Project Overview

This hands-on lab demonstrates an end-to-end **Vendor Due Diligence and Data Processing Agreement (DPA) drafting workflow**.

The project combines vendor security assessment, automated compliance gap analysis, privacy contract drafting, cross-border transfer assessment, and remediation tracking.

The workflow simulates how a security, privacy, procurement, or compliance team can evaluate a third-party service provider before allowing the vendor to process personal data.

### 🔄 End-to-End Workflow

```text
                  ┌─────────────────────────┐
                  │   Vendor Questionnaire  │
                  │    Security Controls    │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │    Vendor Responses     │
                  │       CSV Data          │
                  └────────────┬────────────┘
                               │
                               ▼
                  ┌─────────────────────────┐
                  │   Python Gap Analysis   │
                  │    Pass / Fail / Gap    │
                  └────────────┬────────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
    ┌──────────────────┐              ┌──────────────────┐
    │      DPA Draft   │              │ Cross-Border     │
    │ GDPR/UAE/KSA     │              │ Transfer Addendum│
    └────────┬─────────┘              └────────┬─────────┘
             │                                 │
             └────────────────┬────────────────┘
                              ▼
                    ┌────────────────────┐
                    │ Remediation Tracker│
                    │ Owner / Due Date   │
                    └────────────────────┘
```

---

# 🎯 Objectives

By completing this lab, you will be able to:

* 🔍 Build a vendor security questionnaire
* 📋 Assess vendor responses against a defined control baseline
* 🐍 Use Python to automate compliance gap analysis
* 🚨 Identify missing and failed security controls
* 📄 Draft DPA clauses for data processors
* 🇪🇺 Address GDPR Article 28 requirements
* 🇦🇪 Incorporate UAE PDPL processor considerations
* 🇸🇦 Incorporate KSA PDPL sub-processing considerations
* 🌍 Document cross-border data transfers
* 📑 Create transfer safeguards and contractual requirements
* 📊 Build a remediation tracker
* ⏰ Automatically calculate remediation deadlines based on severity
* 📝 Produce documentation suitable for vendor-risk review

---

# 🧰 Technology Stack

| Technology     | Purpose                                       |
| -------------- | --------------------------------------------- |
| 🐧 Linux       | Lab operating system                          |
| 🐚 Bash        | Automation and file management                |
| 🐍 Python 3    | Questionnaire analysis and tracker automation |
| 📊 CSV         | Questionnaire and remediation data            |
| 🗂️ JSON       | Compliance control baseline                   |
| 📝 Markdown    | DPA and compliance documentation              |
| 📦 Python venv | Isolated Python environment                   |
| 📈 Pandas      | Data processing                               |
| 📋 Tabulate    | CLI table formatting                          |
| 🔐 GDPR        | Processor/DPA requirements                    |
| 🇦🇪 UAE PDPL  | UAE privacy requirements                      |
| 🇸🇦 KSA PDPL  | Saudi privacy requirements                    |

---

# 📋 Prerequisites

Before starting, you should have:

* Basic Linux CLI knowledge
* Familiarity with Bash
* Basic knowledge of CSV and JSON files
* Basic Python knowledge
* Basic understanding of GDPR Article 28
* Basic understanding of UAE PDPL
* Basic understanding of KSA PDPL
* No previous DPA drafting experience is required

---

# 🖥️ Environment Setup

## 🚀 Step 1 — Create the Lab Directory

```bash
mkdir -p ~/vendor-dd-lab/{questionnaire,responses,dpa,tracker}
cd ~/vendor-dd-lab
```

Verify:

```bash
pwd
find . -maxdepth 1 -type d
```

Expected structure:

```text
vendor-dd-lab/
├── questionnaire/
├── responses/
├── dpa/
└── tracker/
```

### ✨ Technology

![Linux](https://img.shields.io/badge/Linux-Environment-E95420?style=flat-square\&logo=linux\&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Automation-4EAA25?style=flat-square\&logo=gnu-bash\&logoColor=white)

---

# 🐍 Step 2 — Create a Python Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Your terminal should show the virtual environment name.

Install required packages:

```bash
pip install pandas tabulate
```

Verify:

```bash
pip list
```

### ✨ Technology

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square\&logo=python\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square\&logo=pandas\&logoColor=white)

---

# 📝 Task 1 — Create and Send the Security Questionnaire

## 🎯 Objective

Create a standardized questionnaire that can be sent to a prospective vendor to evaluate security, privacy, and data-processing controls.

---

## 📄 Step 1.1 — Create the Questionnaire

Run:

```bash
cat > questionnaire/security_questionnaire.csv << 'EOF'
control_id,control_domain,question,response,evidence_link
C1,Access Control,Do you enforce MFA for all admin access?,,
C2,Encryption,Is data encrypted at rest using AES-256 or equivalent?,,
C3,Encryption,Is data encrypted in transit (TLS 1.2+)?,,
C4,Sub-processing,Do you use sub-processors? List all with location.,,
C5,Data Residency,Where is data physically stored/processed?,,
C6,Breach Notification,What is your breach notification SLA (hours)?,,
C7,Data Deletion,Can you certify deletion within 30 days of contract end?,,
C8,Audit Rights,Do you permit client audits or independent assessments?,,
EOF
```

Inspect:

```bash
cat questionnaire/security_questionnaire.csv
```

### Questionnaire Domains

| Control | Domain              | Purpose                    |
| ------- | ------------------- | -------------------------- |
| C1      | Access Control      | MFA protection             |
| C2      | Encryption          | Encryption at rest         |
| C3      | Encryption          | Encryption in transit      |
| C4      | Sub-processing      | Third-party processors     |
| C5      | Data Residency      | Processing locations       |
| C6      | Breach Notification | Incident notification      |
| C7      | Data Deletion       | Secure deletion            |
| C8      | Audit Rights        | Customer assessment rights |

### ✨ Technology

![CSV](https://img.shields.io/badge/CSV-Questionnaire-217346?style=flat-square)

---

# 📤 Step 1.2 — Simulate Sending the Questionnaire

Copy the questionnaire into the vendor response directory:

```bash
cp questionnaire/security_questionnaire.csv \
responses/vendor_acme_response.csv
```

Record the activity:

```bash
echo "Questionnaire sent to vendor_acme@mockvendor.test on $(date)" \
>> tracker/activity_log.txt
```

Verify:

```bash
cat tracker/activity_log.txt
```

---

# 🏢 Step 1.3 — Simulate Vendor Responses

Open:

```bash
nano responses/vendor_acme_response.csv
```

Populate the `response` and `evidence_link` fields.

Example responses:

```text
C1 → Yes, MFA enforced
C2 → Yes, AES-256 encryption at rest
C3 → Yes, TLS 1.2+ enforced
C4 → Yes - AWS (Ireland), SubProcessor-X (India)
C5 → Ireland and India
C6 → Notification within 48 hours
C7 → [leave blank]
C8 → Yes, annual independent assessment permitted
```

### ⚠️ Intentional Gaps

The simulated vendor response intentionally contains gaps:

```text
C4 → Incomplete sub-processor disclosure
C7 → Missing deletion commitment
```

These gaps will be detected automatically in the next task.

---

# 🔍 Task 2 — Review Responses Against the Control Baseline

## 🎯 Objective

Create an automated Python-based compliance review process.

The script will compare vendor answers against required keywords and assign:

```text
PASS
FAIL
MISSING
N/A
```

---

# 📋 Step 2.1 — Create the Control Baseline

Create:

```bash
cat > tracker/baseline.json << 'EOF'
{
  "C1": {
    "required_keyword": "MFA",
    "severity": "High"
  },
  "C2": {
    "required_keyword": "AES-256",
    "severity": "High"
  },
  "C3": {
    "required_keyword": "TLS",
    "severity": "High"
  },
  "C4": {
    "required_keyword": "location",
    "severity": "Critical"
  },
  "C6": {
    "required_keyword": "hours",
    "severity": "Medium"
  },
  "C7": {
    "required_keyword": "30 days",
    "severity": "High"
  }
}
EOF
```

Validate the JSON:

```bash
python3 -m json.tool tracker/baseline.json
```

### ✨ Technology

![JSON](https://img.shields.io/badge/JSON-Control%20Baseline-000000?style=flat-square\&logo=json\&logoColor=white)

---

# 🐍 Step 2.2 — Build the Gap Analysis Script

Create:

```bash
nano tracker/review_responses.py
```

Use:

```python
import csv
import json


def load_baseline(path: str) -> dict:
    """Load control baseline JSON."""

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def review_response(row: dict, baseline: dict) -> str:
    """
    Compare a questionnaire row against the baseline.

    Returns:
        PASS, FAIL, MISSING, or N/A
    """

    control_id = row["control_id"]
    response = row["response"].strip()

    if not response:
        return "MISSING"

    if control_id not in baseline:
        return "N/A"

    required_keyword = baseline[
        control_id
    ]["required_keyword"]

    if required_keyword.lower() in response.lower():
        return "PASS"

    return "FAIL"


def generate_report(
    csv_path: str,
    baseline_path: str,
    output_path: str
):
    """Generate vendor compliance gap report."""

    baseline = load_baseline(baseline_path)

    with open(
        csv_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    fieldnames = reader.fieldnames + [
        "status",
        "severity"
    ]

    results = []

    for row in rows:

        status = review_response(
            row,
            baseline
        )

        severity = baseline.get(
            row["control_id"],
            {}
        ).get(
            "severity",
            ""
        )

        row["status"] = status
        row["severity"] = severity

        results.append(row)

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":

    generate_report(
        "../responses/vendor_acme_response.csv",
        "baseline.json",
        "vendor_acme_gap_report.csv"
    )

    print("Vendor gap analysis completed.")
```

> **Note:** Because the script is executed from inside `tracker/`, the response path uses `../responses/`.

---

# ▶️ Step 2.3 — Run the Gap Analysis

```bash
cd ~/vendor-dd-lab/tracker
python3 review_responses.py
```

Expected:

```text
Vendor gap analysis completed.
```

Check the report:

```bash
column -s, -t < vendor_acme_gap_report.csv | less
```

---

# 🚨 Step 2.4 — Review Compliance Gaps

Search for failures:

```bash
grep -E "FAIL|MISSING" vendor_acme_gap_report.csv
```

Expected results should include:

```text
C4 → FAIL → Critical
C7 → MISSING → High
```

### Gap Analysis Model

```text
Vendor Response
       │
       ▼
Required Keyword
       │
       ├── Found ──────► PASS
       │
       ├── Not Found ──► FAIL
       │
       └── Empty ──────► MISSING
```

### ✨ Technology

![Python](https://img.shields.io/badge/Python-Gap%20Analysis-3776AB?style=flat-square\&logo=python\&logoColor=white)

---

# 📄 Task 3 — Draft DPA Clauses

## 🎯 Objective

Create a Data Processing Agreement addressing:

* GDPR Article 28
* Processor obligations
* Sub-processor flow-down
* UAE PDPL considerations
* KSA PDPL considerations
* Audit rights
* Breach notification
* Data deletion

> ⚠️ The DPA produced in this lab is an educational draft, not legal advice. Actual contractual language should be reviewed and approved by qualified privacy/legal counsel.

---

# 📝 Step 3.1 — Create the DPA

```bash
nano dpa/DPA_draft.md
```

Recommended structure:

```markdown
# Data Processing Agreement (Draft)

## 1. Subject Matter and Duration

This Data Processing Agreement ("DPA") governs the processing
of personal data by the Processor on behalf of the Controller
during the term of the applicable services agreement.

The Processor shall process personal data only for the purposes
and duration documented by the Controller.

## 2. Nature and Purpose of Processing

The processing may include customer account management,
service delivery, support, authentication, security monitoring,
and other documented processing activities.

Categories of data subjects may include customers, users,
employees, contractors, and business contacts.

Categories of personal data may include identity information,
contact information, account information, technical data,
and other information specified in the applicable processing
instructions.

## 3. Processor Obligations

The Processor shall:

- Process personal data only on documented instructions.
- Maintain confidentiality of authorized personnel.
- Implement appropriate technical and organizational measures.
- Apply security controls consistent with GDPR Article 32.
- Assist the Controller with applicable data-subject requests.
- Assist with security incidents and regulatory obligations.
- Maintain appropriate records relating to processing.

The parties should separately confirm the applicable
UAE PDPL processor requirements and contractual obligations
before execution.

The parties should also confirm applicable KSA PDPL
requirements relating to processing and sub-processing.

## 4. Sub-Processor Flow-Down

The Processor shall not appoint a sub-processor without the
authorization mechanism agreed with the Controller.

Where sub-processors are authorized, the Processor shall impose
written data-protection obligations on each sub-processor that
provide equivalent protection to the obligations applicable
to the Processor.

The Processor shall remain responsible for the performance of
its contractual obligations concerning the sub-processor.

The Processor shall provide at least 30 days' prior written
notice of proposed material changes to sub-processors, subject
to the parties' agreed authorization and objection procedure.

The Controller may object to a proposed sub-processor on
reasonable data-protection grounds within the agreed notice
period.

## 5. Cross-Border Transfer

Cross-border transfers shall be performed only where a valid
legal transfer mechanism and appropriate safeguards are in place.

The parties shall document relevant destination countries,
sub-processors, transfer mechanisms, and supplementary safeguards.

## 6. Audit and Assistance

The Processor shall provide information reasonably necessary
to demonstrate compliance with applicable data-protection
obligations.

The Controller may conduct or commission reasonable audits or
assessments subject to appropriate confidentiality, security,
and operational safeguards.

Breach notification timelines shall be defined contractually
and aligned with applicable legal requirements and the parties'
incident-response procedures.

## 7. Data Deletion and Return

At the end of the applicable services, the Processor shall,
subject to legal retention requirements, return or securely
delete personal data within the agreed contractual period.

The Processor shall provide reasonable confirmation of deletion
where contractually required.

The parties should specifically resolve the outstanding C7
vendor response before execution of this DPA.
```

---

# 🔗 Sub-Processor Flow-Down

The DPA should clearly establish:

```text
Controller
     │
     ▼
Processor
     │
     ├── Written Authorization
     │
     ▼
Sub-Processor
     │
     ├── Data Protection Contract
     ├── Security Obligations
     ├── Confidentiality
     ├── Incident Assistance
     └── Deletion / Return
```

### Key Concepts

| Requirement              | Purpose                             |
| ------------------------ | ----------------------------------- |
| Authorization            | Control sub-processor appointments  |
| Flow-down                | Extend privacy obligations          |
| Notice                   | Give controller visibility          |
| Objection                | Allow risk-based challenge          |
| Processor responsibility | Maintain contractual accountability |

---

# 🌍 Task 4 — Cross-Border Transfer Addendum

## 🎯 Objective

Document international data flows discovered during vendor due diligence.

The simulated vendor identified:

```text
AWS → Ireland
SubProcessor-X → India
```

The India location requires additional review of the applicable transfer mechanism and safeguards.

---

# 📝 Step 4.1 — Create the Addendum

```bash
nano dpa/cross_border_addendum.md
```

Use:

```markdown
# Cross-Border Data Transfer Addendum

## 1. Purpose

This Addendum governs international transfers of personal data
performed by the Processor or its approved sub-processors.

## 2. Transfer Mechanism

Each international transfer shall rely on a legally valid
transfer mechanism applicable to the relevant jurisdiction.

Depending on the applicable legal regime, mechanisms may include:

- An applicable adequacy decision
- Standard Contractual Clauses where appropriate
- Approved contractual safeguards
- Other legally recognized transfer mechanisms

The applicable mechanism shall be documented for each transfer.

## 3. Destination Countries

Based on the simulated vendor questionnaire:

- Ireland
- India

The vendor shall maintain an accurate list of countries in
which personal data is stored or processed.

## 4. Safeguards

Where a destination requires additional safeguards, the parties
shall document appropriate contractual, technical, and
organizational measures.

Possible safeguards may include:

- Encryption in transit
- Encryption at rest
- Access controls
- MFA
- Least-privilege access
- Logging and monitoring
- Data minimization
- Incident-response procedures
- Appropriate contractual protections

## 5. KSA PDPL Considerations

Transfers of personal data from Saudi Arabia shall be assessed
against applicable KSA PDPL requirements and current regulatory
guidance.

Where required, the parties shall document the relevant transfer
mechanism, safeguards, and assessment.

## 6. UAE PDPL Considerations

Transfers of personal data from the UAE shall be assessed against
applicable UAE PDPL requirements, including applicable provisions
concerning cross-border transfers and contractual safeguards.

## 7. Sub-Processor Transparency

The Processor shall maintain an up-to-date list of sub-processors,
processing locations, and applicable transfer mechanisms.

Material changes shall be communicated through the agreed
sub-processor notification process.
```

---

# 🔍 Step 4.2 — Connect the Addendum to Gap Findings

Review:

```bash
grep -E "FAIL|MISSING" \
tracker/vendor_acme_gap_report.csv
```

The review should identify issues including:

```text
C4 → Sub-processor/location disclosure
C7 → Data deletion commitment
```

These issues should be reflected in the DPA negotiation and remediation plan.

### ✨ Technology

![GDPR](https://img.shields.io/badge/GDPR-Cross--Border%20Transfers-0052CC?style=flat-square)
![UAE PDPL](https://img.shields.io/badge/UAE%20PDPL-Transfer%20Review-6A1B9A?style=flat-square)
![KSA PDPL](https://img.shields.io/badge/KSA%20PDPL-Transfer%20Review-006C35?style=flat-square)

---

# 📊 Task 5 — Build the Remediation Tracker

## 🎯 Objective

Automatically convert failed or missing controls into remediation tasks.

### Severity-Based SLA

| Severity    | Due Date |
| ----------- | -------: |
| 🔴 Critical |   7 days |
| 🟠 High     |  14 days |
| 🟡 Medium   |  30 days |

---

# 🐍 Step 5.1 — Create Tracker Generator

```bash
nano tracker/build_tracker.py
```

Use:

```python
import csv
from datetime import datetime, timedelta


def build_tracker(
    gap_report_path: str,
    output_path: str
):
    """
    Build a remediation tracker from the gap report.
    """

    severity_days = {
        "Critical": 7,
        "High": 14,
        "Medium": 30
    }

    with open(
        gap_report_path,
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    fieldnames = [
        "control_id",
        "issue",
        "severity",
        "owner",
        "due_date",
        "status"
    ]

    today = datetime.now().date()
    results = []

    for row in rows:

        if row["status"] not in (
            "FAIL",
            "MISSING"
        ):
            continue

        severity = row["severity"]

        days = severity_days.get(
            severity,
            30
        )

        due_date = (
            today + timedelta(days=days)
        ).isoformat()

        results.append({
            "control_id": row["control_id"],
            "issue": row["question"],
            "severity": severity,
            "owner": "TBD",
            "due_date": due_date,
            "status": "Open"
        })

    with open(
        output_path,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    print(
        f"Created {len(results)} remediation items."
    )


if __name__ == "__main__":

    build_tracker(
        "vendor_acme_gap_report.csv",
        "remediation_tracker.csv"
    )
```

---

# ▶️ Step 5.2 — Generate the Tracker

From the tracker directory:

```bash
cd ~/vendor-dd-lab/tracker
python3 build_tracker.py
```

Expected:

```text
Created 2 remediation items.
```

View:

```bash
column -s, -t < remediation_tracker.csv
```

Example:

```text
control_id  issue                         severity  owner  due_date    status
C4          Do you use sub-processors... Critical  TBD    YYYY-MM-DD  Open
C7          Can you certify deletion...  High      TBD    YYYY-MM-DD  Open
```

---

# 👤 Step 5.3 — Assign Owners

Open:

```bash
nano remediation_tracker.csv
```

Replace:

```text
TBD
```

with appropriate owners.

Example:

```text
C4 → Privacy Counsel
C7 → Vendor Manager
```

Possible owners include:

* Privacy Counsel
* Vendor Risk Manager
* Security Engineering
* Procurement
* Legal
* Compliance
* Data Protection Officer

---

# 📂 Final Project Structure

After completing the lab:

```text
vendor-dd-lab/
│
├── questionnaire/
│   └── security_questionnaire.csv
│
├── responses/
│   └── vendor_acme_response.csv
│
├── dpa/
│   ├── DPA_draft.md
│   └── cross_border_addendum.md
│
├── tracker/
│   ├── activity_log.txt
│   ├── baseline.json
│   ├── review_responses.py
│   ├── vendor_acme_gap_report.csv
│   ├── build_tracker.py
│   └── remediation_tracker.csv
│
└── venv/
```

---

# 🧪 Verification

## ✅ Step 1 — Verify All Artifacts

```bash
cd ~/vendor-dd-lab

ls -la questionnaire/
ls -la responses/
ls -la dpa/
ls -la tracker/
```

---

## 🔍 Step 2 — Verify Gap Findings

```bash
grep -E "FAIL|MISSING" \
tracker/vendor_acme_gap_report.csv
```

Expected:

```text
C4 → FAIL
C7 → MISSING
```

---

## 📄 Step 3 — Verify DPA TODOs

```bash
grep -c "TODO" \
dpa/DPA_draft.md \
dpa/cross_border_addendum.md
```

Expected:

```text
0
0
```

> If the documents contain placeholder text that uses a different notation, review them manually as well.

---

## 📊 Step 4 — Verify Remediation Tracker

```bash
wc -l tracker/remediation_tracker.csv
```

The file should contain a header plus the identified remediation items.

---

# 🏆 Final Verification Checklist

* [ ] Vendor questionnaire created
* [ ] Vendor response simulated
* [ ] Activity log created
* [ ] Control baseline created
* [ ] Python gap analysis completed
* [ ] C4 flagged as a compliance gap
* [ ] C7 flagged as a missing response
* [ ] DPA draft created
* [ ] Processor obligations documented
* [ ] Sub-processor flow-down documented
* [ ] Notification and objection mechanisms documented
* [ ] Cross-border transfer addendum created
* [ ] International processing locations documented
* [ ] Transfer safeguards documented
* [ ] Remediation tracker generated
* [ ] Severity-based due dates calculated
* [ ] Remediation owners assigned
* [ ] All TODO markers removed
* [ ] Final artifacts reviewed

---

# 🛠️ Troubleshooting

## ❌ Python CSV Errors

Check the source CSV:

```bash
python3 -c \
"import csv; print(list(csv.DictReader(open('responses/vendor_acme_response.csv'))))"
```

Make sure there are no malformed rows or unexpected commas.

---

## ❌ JSON Validation Error

Run:

```bash
python3 -m json.tool tracker/baseline.json
```

If valid, the formatted JSON will be displayed.

---

## ❌ Python Date Calculation Error

Ensure `timedelta` receives an integer:

```python
timedelta(days=14)
```

Not:

```python
timedelta(days="14")
```

---

## ❌ Gap Report Is Empty

Check the vendor response:

```bash
cat responses/vendor_acme_response.csv
```

Then run:

```bash
python3 tracker/review_responses.py
```

Make sure the script is using the correct relative paths.

---

## ❌ DPA Still Contains TODOs

Search:

```bash
grep -Rni "TODO" dpa/
```

Review every result before considering the document complete.

---

# 🔐 Security and Privacy Controls Demonstrated

| Control                     | Lab Implementation            |
| --------------------------- | ----------------------------- |
| 🔍 Vendor Due Diligence     | Security questionnaire        |
| 📊 Risk Assessment          | Automated gap analysis        |
| 🚨 Gap Identification       | PASS/FAIL/MISSING status      |
| 📄 Contractual Protection   | DPA                           |
| 🔗 Sub-Processor Management | Flow-down clauses             |
| 🌍 Transfer Governance      | Cross-border addendum         |
| 📋 Remediation              | Automated tracker             |
| ⏰ Risk-Based Deadlines      | Severity-based due dates      |
| 👤 Accountability           | Assigned owners               |
| 📝 Evidence                 | CSV, JSON, Markdown artifacts |

---

# 🏛️ Regulatory and Governance Mapping

| Area                       | Technical / Contractual Control         |
| -------------------------- | --------------------------------------- |
| 🇪🇺 GDPR Article 28       | Processor obligations                   |
| 🇪🇺 GDPR Art. 28(2)       | Sub-processor authorization             |
| 🇪🇺 GDPR Art. 28(4)       | Sub-processor flow-down                 |
| 🇦🇪 UAE PDPL              | Processor and transfer considerations   |
| 🇸🇦 KSA PDPL              | Processing/sub-processor considerations |
| 🌍 International Transfers | Transfer mechanism and safeguards       |
| 🔐 Security                | MFA and encryption assessment           |
| 🚨 Incident Management     | Breach notification SLA                 |
| 🗑️ Data Lifecycle         | Deletion requirements                   |
| 🔎 Auditability            | Audit rights                            |
| 📊 Vendor Risk             | Remediation tracking                    |

> ⚠️ Regulatory requirements and official guidance can change. This lab is intended for technical training and should not be used as a substitute for current legal advice or jurisdiction-specific legal review.

---

# 🧠 Skills Demonstrated

```text
🐧 Linux Administration
🐚 Bash Scripting
🐍 Python Automation
📊 CSV Processing
🗂️ JSON Configuration
📋 Vendor Security Assessment
🔍 Compliance Gap Analysis
🚨 Risk Identification
📄 DPA Drafting
🔗 Sub-Processor Governance
🌍 Cross-Border Transfer Assessment
📈 Vendor Risk Management
⏰ SLA/Remediation Automation
🛡️ Privacy Compliance
🇪🇺 GDPR Awareness
🇦🇪 UAE PDPL Awareness
🇸🇦 KSA PDPL Awareness
```

---

# 🚀 Real-World Applications

The techniques demonstrated in this project can support:

* Vendor Risk Management
* Third-Party Risk Management
* Privacy Operations
* Data Protection Programs
* Procurement Security Reviews
* Security Questionnaires
* DPA Preparation
* Privacy Counsel Workflows
* Compliance Assessments
* Supplier Security Reviews
* Cross-Border Transfer Assessments
* Remediation Management
* GDPR readiness programs
* GCC privacy compliance programs

---

# 🌟 Conclusion

This lab implemented a complete **Vendor Due Diligence and DPA Drafting workflow**.

The process begins with a structured security questionnaire, simulates vendor responses, evaluates those responses against a control baseline, identifies compliance gaps, and converts those findings into contractual and remediation actions.

The complete workflow is:

```text
Questionnaire
     ↓
Vendor Response
     ↓
Automated Gap Analysis
     ↓
Risk Identification
     ↓
DPA Drafting
     ↓
Sub-Processor Controls
     ↓
Cross-Border Transfer Review
     ↓
Remediation Tracker
     ↓
Owner + Due Date
     ↓
Compliance Evidence
```

### 🎯 Final Outcome

**Assess → Identify → Contract → Transfer Safely → Remediate → Track**

This project provides practical experience combining **vendor risk management, privacy compliance, Python automation, contract-control mapping, cross-border data governance, and remediation management**.

---

<p align="center">

## 🔐 Assess Vendors • Protect Data • Manage Risk • Demonstrate Compliance

</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Vendor%20Risk-Assessment-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/DPA-GDPR%20%7C%20UAE%20%7C%20KSA-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Automation-Python-orange?style=for-the-badge">
</p>
