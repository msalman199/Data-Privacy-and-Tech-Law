<div align="center">

# 📋 KSA PDPL Compliance Gap Assessment

![PDPL](https://img.shields.io/badge/KSA-PDPL-006C35?style=for-the-badge)
![SDAIA](https://img.shields.io/badge/SDAIA-Regulations-1E90FF?style=for-the-badge)
![LibreOffice](https://img.shields.io/badge/LibreOffice-Calc-18A303?style=for-the-badge&logo=libreoffice&logoColor=white)
![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-Terminal-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**A hands-on compliance gap assessment against the Saudi Personal Data Protection Law**

</div>

---

## 📑 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [⚙️ Environment Setup](#️-environment-setup)
- [📚 Task 1: Prepare Local PDPL Reference Material](#-task-1-prepare-local-pdpl-reference-material)
- [📊 Task 2: Build the Control Scoring Spreadsheet](#-task-2-build-the-control-scoring-spreadsheet)
- [🐍 Task 3: Map Gaps and Calculate Risk Priority](#-task-3-map-gaps-and-calculate-risk-priority)
- [🎯 Task 4: Prioritize Remediation by Risk and Effort](#-task-4-prioritize-remediation-by-risk-and-effort)
- [📄 Task 5: Produce the Board-Ready Roadmap](#-task-5-produce-the-board-ready-roadmap)
- [🔍 Verification](#-verification)
- [📚 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | Interpret key KSA PDPL articles and map them to organizational controls |
| 2 | Build a scoring spreadsheet to assess compliance maturity using LibreOffice Calc |
| 3 | Identify and prioritize compliance gaps against SDAIA implementing regulations |
| 4 | Produce a structured, board-ready remediation roadmap document |

## ✅ Prerequisites

| Area | Requirement |
|------|-------------|
| 🔐 Privacy Concepts | Basic familiarity with data protection concepts (data subject rights, lawful basis, breach notification) |
| 🐧 Linux Basics | Comfortable with Linux terminal navigation and text editors |
| 📜 PDPL Knowledge | No prior SDAIA/PDPL-specific knowledge required, but review of general privacy law concepts is helpful |

## 🖥️ Lab Environment

> 💻 **Provided by Al Nafi:** A single Linux machine via **Start Lab**.

---

## ⚙️ Environment Setup

```bash
# 📦 Update package index and install required tools
sudo apt update
sudo apt install -y libreoffice-calc poppler-utils wget nano

# 📁 Create lab working directory
mkdir -p ~/pdpl-lab/{docs,assessment,roadmap}
cd ~/pdpl-lab
```

> ℹ️ `poppler-utils` provides `pdftotext` for extracting text from PDF articles. `libreoffice-calc` will be used to build the scoring matrix.

---

## 📚 Task 1: Prepare Local PDPL Reference Material

> 🧭 Since we assess against publicly known PDPL structure, create local reference files summarizing key articles (simulating your "local PDFs").

```bash
# 📂 Navigate to the docs directory
cd ~/pdpl-lab/docs

# 📝 Open the reference summary file
nano pdpl_articles_summary.txt
```

Populate with a structured summary. Use this starter template and complete it with **at least 8 articles**:

```text
KSA PDPL - KEY ARTICLES SUMMARY (Reference)
=============================================
Article 5  - Lawful basis for processing personal data
Article 6  - Consent requirements and withdrawal
Article 12 - Purpose limitation
Article 13 - Data minimization
Article 19 - Data subject access rights
Article 20 - Right to correction and deletion
Article 21 - Cross-border data transfer restrictions
Article 24 - Breach notification requirement (72 hours to SDAIA)
# TODO: Add articles on data retention, DPO appointment,
# and processor obligations (research SDAIA public guidance)
```

Convert any sample PDF (if provided in `/opt/lab-files/`) to text for review:

```bash
# 📄 If a sample regulation PDF exists in the lab environment
pdftotext /opt/lab-files/sdaia_regulation_sample.pdf ~/pdpl-lab/docs/sdaia_reg.txt 2>/dev/null || echo "No sample PDF found - proceed with manual summary"

# 👀 Review your summary
cat ~/pdpl-lab/docs/pdpl_articles_summary.txt
```

---

## 📊 Task 2: Build the Control Scoring Spreadsheet

> 🧭 Create a scoring workbook to evaluate the sample SaaS startup's current controls.

```bash
# 📂 Navigate to the assessment directory
cd ~/pdpl-lab/assessment

# 📊 Launch LibreOffice Calc
libreoffice --calc gap_assessment.ods &
```

Build a spreadsheet with these columns (create manually in Calc):

| Column | Description |
|--------|-------------|
| Article Ref | PDPL article number |
| Control Requirement | What the article mandates |
| Current State | None / Partial / Full |
| Score (0-3) | 0=None, 1=Basic, 2=Partial, 3=Compliant |
| Evidence | Notes on current implementation |
| Risk Level | High / Medium / Low |

> 🏢 **Sample startup profile** (use this fictional context for scoring):
>
> **Company: CloudNest SaaS** (KSA-based HR tech startup)
> - Stores employee PII of client companies across GCC
> - No formal DPO appointed
> - Consent captured via checkbox, no withdrawal mechanism
> - Data hosted on regional cloud provider, some backups in EU
> - No documented breach response plan
> - Basic access controls, no data retention policy

**📝 TODO for students:**

- Score all 8+ articles from Task 1 against CloudNest's profile
- Save file as `gap_assessment.ods`
- Export a CSV summary for scripting in Task 3:

```bash
# 💾 Export your scored sheet to CSV via LibreOffice UI (File > Save As > CSV)
# 🔎 Confirm the file exists
ls -la ~/pdpl-lab/assessment/gap_assessment.csv
```

---

## 🐍 Task 3: Map Gaps and Calculate Risk Priority

> 🧭 Write a Python script to process your CSV and flag priority gaps.

```bash
# 📂 Navigate to the assessment directory
cd ~/pdpl-lab/assessment

# 📝 Open the script file
nano gap_analyzer.py
```

Complete this template:

```python
import csv

def load_assessment(csv_path: str) -> list:
    """
    Load the gap assessment CSV into a list of dictionaries.

    Args:
        csv_path: Path to the exported gap_assessment.csv

    Returns:
        List of row dictionaries with keys matching CSV headers
    """
    # TODO: Open the CSV file and use csv.DictReader
    # TODO: Return the list of rows
    pass


def calculate_priority(rows: list) -> list:
    """
    Assign a priority label based on Score and Risk Level.

    Rule of thumb:
      - Score 0-1 AND Risk High  -> "Critical - Immediate"
      - Score 0-1 AND Risk Medium -> "High - 30 days"
      - Score 2 AND any Risk      -> "Medium - 90 days"
      - Score 3                   -> "Monitor"

    Args:
        rows: List of assessment row dicts

    Returns:
        Same list with an added 'Priority' key per row
    """
    # TODO: Iterate over rows, read Score and Risk Level fields
    # TODO: Apply the priority rules above
    # TODO: Return updated rows
    pass


def print_report(rows: list) -> None:
    """Print a simple formatted gap report to the terminal."""
    # TODO: Loop through rows and print Article Ref, Score, Priority
    pass


if __name__ == "__main__":
    data = load_assessment("gap_assessment.csv")
    prioritized = calculate_priority(data)
    print_report(prioritized)
```

Run and validate your script:

```bash
# ▶️ Execute the gap analyzer
python3 gap_analyzer.py
```

> ⚠️ **Troubleshooting:**
> - `FileNotFoundError`: confirm CSV export path matches script location
> - Empty output: check CSV header names match exactly (`Score`, `Risk Level`)

---

## 🎯 Task 4: Prioritize Remediation by Risk and Effort

> 🧭 Create an effort-vs-risk matrix to sequence remediation work.

```bash
# 📂 Navigate to the roadmap directory
cd ~/pdpl-lab/roadmap

# 📝 Open the remediation matrix file
nano remediation_matrix.txt
```

Use this structure and complete it based on your Task 3 output:

```text
REMEDIATION PRIORITIZATION MATRIX
===================================
Gap Item                  | Risk   | Effort | Priority Quadrant
---------------------------------------------------------------
No DPO appointed           | High   | Low    | Quick Win
No breach response plan    | High   | Medium | Do Next
# TODO: Add remaining gaps from your analyzer output
# TODO: Classify each into: Quick Win / Do Next / Plan / Deprioritize
```

**⚖️ Quadrant logic:**

- **Quick Win:** High risk, low effort → do immediately
- **Do Next:** High risk, medium/high effort → schedule within quarter
- **Plan:** Low/medium risk, high effort → long-term roadmap
- **Deprioritize:** Low risk, low urgency

---

## 📄 Task 5: Produce the Board-Ready Roadmap

> 🧭 Compile findings into a final markdown report.

```bash
# 📂 Navigate to the roadmap directory
cd ~/pdpl-lab/roadmap

# 📝 Open the roadmap report file
nano PDPL_Remediation_Roadmap.md
```

Minimum required sections (complete each):

```markdown
# CloudNest SaaS - PDPL Remediation Roadmap

## Executive Summary
<!-- TODO: 3-4 sentences on overall compliance posture -->

## Assessment Scope
<!-- TODO: Articles reviewed, methodology used -->

## Key Findings
<!-- TODO: Top 5 gaps with risk ratings -->

## Remediation Roadmap
| Phase | Timeline | Action Items | Owner |
|---|---|---|---|
| Phase 1 (0-30 days) | | | |
| Phase 2 (30-90 days) | | | |
| Phase 3 (90+ days) | | | |

## Resource Requirements
<!-- TODO: Estimated budget/headcount notes -->
```

---

## 🔍 Verification

Confirm all deliverables exist on the machine:

```bash
cd ~/pdpl-lab
echo "--- Docs ---" && ls docs/
echo "--- Assessment ---" && ls assessment/
echo "--- Roadmap ---" && ls roadmap/

# ▶️ Confirm script runs without error
python3 assessment/gap_analyzer.py

# 🔢 Confirm roadmap has minimum required sections
grep -c "^##" roadmap/PDPL_Remediation_Roadmap.md
```

**Expected outcomes:**

- `gap_assessment.ods` and exported `.csv` with 8+ scored articles
- Working `gap_analyzer.py` producing a priority-labeled report
- Completed `remediation_matrix.txt` with quadrant classifications
- Finished `PDPL_Remediation_Roadmap.md` with all sections filled in

---

## 📚 Key Concepts

| Concept | Description |
|---------|-------------|
| **KSA PDPL** | Saudi Arabia's Personal Data Protection Law governing collection, processing, and transfer of personal data |
| **SDAIA** | Saudi Data & AI Authority — the regulator issuing PDPL implementing regulations |
| **DPO** | Data Protection Officer — a role many PDPL-regulated organizations must formally appoint |
| **Gap Assessment** | Structured comparison of current controls against regulatory requirements to surface deficiencies |
| **Compliance Maturity Scoring** | Rating current-state controls (e.g., 0-3 scale) to quantify how far an organization is from full compliance |
| **Risk-Based Prioritization** | Sequencing remediation work by combining risk severity with implementation effort |
| **Quick Win / Do Next / Plan / Deprioritize** | A four-quadrant model for sequencing remediation by risk vs. effort |
| **Remediation Roadmap** | A phased, board-ready plan translating technical gaps into timelines, owners, and resourcing |

---

## 🏁 Conclusion

In this lab, you performed an end-to-end PDPL compliance gap assessment for a simulated SaaS startup. You reviewed core PDPL article requirements, built a scoring matrix in LibreOffice Calc, automated gap prioritization with a Python script, and translated technical findings into a prioritized, board-ready remediation roadmap.

### 🏆 Key Accomplishments

- ✅ Mapped 8+ KSA PDPL articles to organizational control requirements
- ✅ Built a LibreOffice Calc scoring matrix to assess compliance maturity
- ✅ Automated gap prioritization with a Python risk-scoring script
- ✅ Sequenced remediation work using a risk-vs-effort quadrant model
- ✅ Produced a board-ready remediation roadmap document

### 🌍 Real-World Applications

- 🏢 Running compliance gap assessments for KSA/GCC-regulated organizations
- 📊 Building repeatable scoring frameworks for privacy program maturity
- 🗺️ Translating technical findings into executive-level remediation plans
- 📋 Supporting Compliance Manager responsibilities and IAPP CIPM / ISO 27701 competency areas around gap analysis, risk-based prioritization, and privacy program reporting

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Training-1E90FF?style=for-the-badge)

</div>
