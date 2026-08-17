<div align="center">

# 💳 UAE PDPL Readiness for a Fintech Platform

![UAE PDPL](https://img.shields.io/badge/UAE-PDPL-00732F?style=for-the-badge)
![Federal Decree-Law 45](https://img.shields.io/badge/Federal%20Decree--Law-45%20of%202021-C8102E?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Fintech](https://img.shields.io/badge/Domain-Fintech-6A5ACD?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Terminal-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**Building a PDPL readiness dossier for a simulated UAE fintech platform**

</div>

---

## 📑 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [⚙️ Environment Setup](#️-environment-setup)
- [📊 Task 1: Inventory Personal Data Flows](#-task-1-inventory-personal-data-flows)
- [⚖️ Task 2: Lawful Basis & DPO Appointment Plan](#️-task-2-lawful-basis--dpo-appointment-plan)
- [✅ Task 3: Consent and Rights Workflows](#-task-3-consent-and-rights-workflows)
- [🚨 Task 4: Breach Notification Procedure](#-task-4-breach-notification-procedure)
- [📁 Task 5: Compile the PDPL Compliance Dossier](#-task-5-compile-the-pdpl-compliance-dossier)
- [🔍 Verification](#-verification)
- [📚 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | Map personal data flows in a sample fintech system, including Emirates ID data |
| 2 | Document lawful bases for processing and a DPO appointment plan aligned to Federal Decree-Law 45 of 2021 |
| 3 | Build simple consent and data subject rights (DSAR) handling scripts |
| 4 | Draft a breach notification procedure with timelines |
| 5 | Compile a UAE PDPL compliance dossier |

## ✅ Prerequisites

| Area | Requirement |
|------|-------------|
| 🐧 Linux Basics | Basic Linux command-line familiarity |
| 🐍 Python Basics | Basic Python 3 knowledge (functions, dictionaries, file I/O) |
| 🔐 Privacy Concepts | Conceptual understanding of data protection principles (lawful basis, consent, DSARs, breach notification) |
| 📜 PDPL Knowledge | No prior UAE PDPL expertise required, but review Federal Decree-Law 45 of 2021 summary before starting |

## 🖥️ Lab Environment

> 💻 **Provided by Al Nafi:** A single Linux machine via **Start Lab**.

---

## ⚙️ Environment Setup

```bash
# 📁 Create lab working directory
mkdir -p ~/pdpl-lab/{data,scripts,docs}
cd ~/pdpl-lab

# 🐍 Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 📦 Install required packages
pip install pandas faker jsonschema
```

Verify Python and pip are working:

```bash
# ✅ Confirm interpreter version
python3 --version

# ✅ Confirm packages installed
pip list | grep -E "pandas|faker|jsonschema"
```

---

## 📊 Task 1: Inventory Personal Data Flows

> 🧭 Simulate a fintech data inventory using a CSV file and a Python script that classifies data sensitivity.

Create `~/pdpl-lab/data/data_inventory.csv` with these columns: `data_element,source_system,storage_location,processing_purpose,is_emirates_id,retention_days`

Add **at least 8 rows** covering: Emirates ID number, full name, phone number, transaction history, IP address, KYC documents, bank account number, device fingerprint.

```bash
# 📝 Open the inventory file
nano ~/pdpl-lab/data/data_inventory.csv
```

Create `scripts/classify_data.py`:

```python
import pandas as pd

def classify_sensitivity(row: dict) -> str:
    """
    Classify a data element as 'critical', 'sensitive', or 'standard'
    based on UAE PDPL-style criteria.

    Args:
        row: dictionary representing one CSV row

    Returns:
        Classification string
    """
    # TODO: mark is_emirates_id == True/"True" as 'critical'
    # TODO: mark financial data (transaction/account) as 'sensitive'
    # TODO: everything else as 'standard'
    pass

def generate_report(csv_path: str, output_path: str) -> None:
    """
    Read inventory CSV, classify each row, and write a summary report.
    """
    # TODO: load CSV with pandas
    # TODO: apply classify_sensitivity to each row
    # TODO: write counts per classification and full table to output_path
    pass

if __name__ == "__main__":
    generate_report("../data/data_inventory.csv", "../docs/data_flow_report.txt")
```

Run it:

```bash
# ▶️ Execute the classifier
cd ~/pdpl-lab/scripts
python3 classify_data.py

# 👀 Review the generated report
cat ../docs/data_flow_report.txt
```

---

## ⚖️ Task 2: Lawful Basis & DPO Appointment Plan

Create `docs/lawful_basis_dpo_plan.md`. For each data element in your inventory, document:

- Lawful basis (consent, contract necessity, legal obligation, legitimate interest)
- Justification (1 sentence)
- Whether a DPO is mandatory per **Article 10** (large-scale sensitive data processing)

Template to complete:

```markdown
## Lawful Basis Register
| Data Element | Lawful Basis | Justification |
|---|---|---|
| Emirates ID | ... | ... |

## DPO Appointment Plan
- Trigger criteria met? (Yes/No + reasoning)
- Proposed DPO reporting line:
- Key DPO responsibilities (list 4):
- Anticipated Data Office registration steps:
```

---

## ✅ Task 3: Consent and Rights Workflows

> 🧭 Build a minimal consent record store and DSAR handler using JSON.

Create `scripts/consent_manager.py`:

```python
import json
import uuid
from datetime import datetime
from pathlib import Path

CONSENT_STORE = Path("../data/consents.json")

def record_consent(user_id: str, purpose: str, granted: bool) -> dict:
    """
    Record a consent event for a user and persist to CONSENT_STORE.

    Returns:
        The consent record dictionary created.
    """
    # TODO: build record with consent_id (uuid4), user_id, purpose,
    #       granted, timestamp (ISO format)
    # TODO: load existing JSON list (create empty list if file missing)
    # TODO: append and save back to CONSENT_STORE
    pass

def handle_dsar(user_id: str, request_type: str) -> str:
    """
    Simulate handling a Data Subject Access Request.
    request_type: one of 'access', 'erasure', 'rectification'

    Returns:
        A status message confirming action and legal deadline (30 days).
    """
    # TODO: validate request_type against allowed values
    # TODO: return message including a calculated due date
    pass

if __name__ == "__main__":
    record_consent("user123", "marketing_emails", True)
    print(handle_dsar("user123", "access"))
```

Run and inspect output:

```bash
# ▶️ Execute the consent manager
python3 consent_manager.py

# 👀 Inspect the persisted consent record
cat ../data/consents.json
```

---

## 🚨 Task 4: Breach Notification Procedure

Create `docs/breach_notification_procedure.md` covering:

- Detection and internal escalation steps (who is notified, within what timeframe)
- Assessment criteria for "high risk to individuals"
- Notification timeline to UAE Data Office (draft based on anticipated 72-hour style requirement)
- Data subject notification criteria and template message
- Post-incident review steps

Use this skeleton and complete each section with 2-4 bullet points:

```markdown
# Breach Notification Procedure

## 1. Detection & Escalation
## 2. Risk Assessment Criteria
## 3. Regulator Notification (UAE Data Office)
## 4. Data Subject Notification
## 5. Post-Incident Review
```

---

## 📁 Task 5: Compile the PDPL Compliance Dossier

> 🧭 Combine all artifacts into a single dossier folder and generate an index.

```bash
# 📂 Review what's been produced so far
cd ~/pdpl-lab
ls docs/ data/
```

Create `scripts/build_dossier.py`:

```python
from pathlib import Path
from datetime import date

def build_index(docs_dir: str, data_dir: str, output_file: str) -> None:
    """
    Generate an index Markdown file listing all dossier components
    with completion status and today's date.
    """
    # TODO: list files in docs_dir and data_dir
    # TODO: write a Markdown index with headings:
    #       "UAE PDPL Compliance Dossier", generated date,
    #       and a checklist of the 5 required artifacts
    pass

if __name__ == "__main__":
    build_index("docs", "data", "docs/dossier_index.md")
```

Run:

```bash
# ▶️ Execute the dossier builder
cd scripts
python3 build_dossier.py

# 👀 Review the generated index
cat ../docs/dossier_index.md
```

---

## 🔍 Verification

Confirm your work on the same machine:

```bash
# 📁 Check all required files exist
ls ~/pdpl-lab/data/data_inventory.csv
ls ~/pdpl-lab/docs/lawful_basis_dpo_plan.md
ls ~/pdpl-lab/docs/breach_notification_procedure.md
ls ~/pdpl-lab/data/consents.json
ls ~/pdpl-lab/docs/dossier_index.md

# ✅ Validate JSON structure
python3 -c "import json; json.load(open('~/pdpl-lab/data/consents.json'.replace('~', '/root')))"
```

**Expected outcomes:**

- `data_flow_report.txt` shows counts of critical/sensitive/standard data elements
- `consents.json` contains at least one valid consent record with uuid and timestamp
- `dossier_index.md` lists all 5 artifacts with status markers
- Both Markdown documents contain completed (non-placeholder) content

<details>
<summary>⚠️ Troubleshooting</summary>

- **ModuleNotFoundError:** ensure venv is activated (`source ~/pdpl-lab/venv/bin/activate`)
- **Empty JSON errors:** confirm `consents.json` initializes as `[]` before first append
- **CSV parsing errors:** check for extra commas or missing headers in `data_inventory.csv`

</details>

---

## 📚 Key Concepts

| Concept | Description |
|---------|-------------|
| **UAE PDPL** | Federal Decree-Law 45 of 2021 — the UAE's federal Personal Data Protection Law |
| **UAE Data Office** | The federal regulator overseeing PDPL compliance and breach notifications |
| **DPO Appointment Trigger (Article 10)** | Criteria requiring a Data Protection Officer where large-scale sensitive data processing occurs |
| **Lawful Basis** | The legal justification (consent, contract necessity, legal obligation, legitimate interest) for processing personal data |
| **DSAR** | Data Subject Access Request — access, erasure, or rectification requests with a defined statutory deadline |
| **Consent Management** | Recording, timestamping, and persisting user consent events for auditability |
| **Breach Notification Timeline** | Structured escalation, assessment, and notification procedure anticipating short (72-hour style) regulatory windows |
| **Compliance Dossier** | A consolidated, indexed set of artifacts demonstrating PDPL readiness |

---

## 🏁 Conclusion

In this lab, you built a working simulation of PDPL readiness activities for a fintech platform. You inventoried and classified personal data flows including Emirates ID data, documented lawful bases and a DPO appointment plan, implemented consent recording and DSAR handling logic in Python, drafted a breach notification procedure anticipating UAE Data Office requirements, and compiled all artifacts into a structured compliance dossier.

### 🏆 Key Accomplishments

- ✅ Built a classified fintech personal-data inventory including Emirates ID data
- ✅ Documented a lawful-basis register and DPO appointment plan under Article 10
- ✅ Implemented Python-based consent recording and DSAR handling logic
- ✅ Drafted a breach notification procedure anticipating UAE Data Office timelines
- ✅ Compiled a structured, indexed UAE PDPL compliance dossier

### 🌍 Real-World Applications

- 🏦 Preparing fintech platforms for UAE PDPL readiness assessments
- 🆔 Handling high-sensitivity identifiers like Emirates ID under region-specific data protection law
- 📋 Supporting DPO and Compliance Officer responsibilities
- 🎓 Reinforcing concepts tested in IAPP CIPP/E and CIPM certifications

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Training-1E90FF?style=for-the-badge)

</div>
