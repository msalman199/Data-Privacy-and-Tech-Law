<div align="center">

# 🛡️ Mapping Personal Data Inventory for GDPR Compliance

![GDPR](https://img.shields.io/badge/GDPR-003399?style=for-the-badge&logo=europeanunion&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

*A beginner-friendly lab: build a Record of Processing Activities (RoPA) using CSV and Python*

</div>

---

## 📖 Table of Contents

- [🎯 Objectives](#-objectives)
- [📋 Prerequisites](#-prerequisites)
- [📚 Key Terms](#-key-terms)
- [🖥️ Lab Environment](#️-lab-environment)
- [📝 Task 1: Create the Data Inventory CSV Template](#-task-1-create-the-data-inventory-csv-template)
- [➕ Task 2: Enumerate Additional Data Sources](#-task-2-enumerate-additional-data-sources)
- [🏷️ Task 3: Tag and Verify Sensitive Categories](#️-task-3-tag-and-verify-sensitive-categories)
- [✔️ Task 4: Validate Lawful Basis and Retention Fields](#️-task-4-validate-lawful-basis-and-retention-fields)
- [📤 Task 5: Generate an Exportable RoPA Report](#-task-5-generate-an-exportable-ropa-report)
- [✅ Verification](#-verification)
- [🔧 Troubleshooting](#-troubleshooting)
- [🔑 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Objectives

| # | By the end of this lab, you will be able to... |
|---|---|
| 1 | Build a simple Record of Processing Activities (RoPA) using a CSV-based data inventory |
| 2 | Identify data sources, data subject categories, and processing purposes |
| 3 | Tag sensitive/special category data (biometric, health) |
| 4 | Document lawful basis and retention periods per GDPR Article 30 and GCC PDPL |
| 5 | Export a RoPA report for review by a Data Protection Officer (DPO) |

## 📋 Prerequisites

| Requirement | Details |
|---|---|
| Linux terminal | Basic familiarity — navigating folders, editing files |
| Privacy/legal knowledge | None required — key terms are explained below |
| Environment | A single Linux machine (provided via Start Lab) |

## 📚 Key Terms

| Term | Definition |
|---|---|
| RoPA | Record of Processing Activities — a log of how personal data is used |
| Data Subject | The person the data belongs to (e.g., customer, employee) |
| Lawful Basis | The legal reason for processing data under GDPR (e.g., consent, contract) |
| Special Category Data | Sensitive data like health, biometric, or religious data |

## 🖥️ Lab Environment

> Your Al Nafi Linux machine is ready to use. This lab uses a lightweight CSV + command-line approach (no cloud dependencies, no complex installs) so you can focus on the compliance concepts.

```bash
# 📁 Create and move into a folder for this lab
mkdir -p ~/gdpr-lab
cd ~/gdpr-lab
```

```bash
# 🐍 Check Python version (used later to generate the report)
python3 --version

# ✏️ Check that nano editor is available (or use vim/gedit if preferred)
nano --version
```

If Python 3 is missing, install it:

```bash
sudo apt update
sudo apt install -y python3 python3-pip
```

---

## 📝 Task 1: Create the Data Inventory CSV Template

> We will use a CSV file instead of installing OpenMetadata, to keep this beginner-friendly and lightweight.

```bash
# 📄 Create the CSV file with header row
nano data_inventory.csv
```

Copy this header row and sample data into the file, then save (`Ctrl+O`, `Enter`, `Ctrl+X`):

```csv
process_id,process_name,data_source,data_subject_category,personal_data_fields,sensitive_category,processing_purpose,lawful_basis,retention_period
1,Employee Payroll,HR System,Employees,"Name, Bank Account, Salary",No,Salary payment,Contract,7 years
2,Customer Support Tickets,Helpdesk App,Customers,"Name, Email, Complaint text",No,Issue resolution,Legitimate Interest,2 years
3,Health Insurance Claims,Insurance Portal,Employees,"Name, Medical Condition",Yes-Health,Insurance claim processing,Consent,5 years
```

**Explanation of columns:**
- `sensitive_category`: Marks `"Yes-Health"`, `"Yes-Biometric"`, or `"No"`
- `lawful_basis`: One of `Consent`, `Contract`, `Legal Obligation`, `Vital Interest`, `Public Task`, `Legitimate Interest`
- `retention_period`: How long data is kept before deletion

---

## ➕ Task 2: Enumerate Additional Data Sources

Add three more rows representing a fictional organization's other systems (e.g., CRM, biometric access control, marketing platform).

```bash
# ✏️ Reopen the CSV to add rows
nano data_inventory.csv
```

Example rows to add:

```csv
4,Office Access Control,Biometric Scanner,Employees,"Fingerprint Template",Yes-Biometric,Building security,Legitimate Interest,1 year
5,Marketing Newsletter,Email Platform,Customers,"Name, Email",No,Marketing communication,Consent,Until withdrawal
```

> **TODO:** Add one more row of your own for a "Website Cookies" process (data source: Website, data subject: Website Visitors)

---

## 🏷️ Task 3: Tag and Verify Sensitive Categories

Use a simple command to check that all sensitive rows are correctly tagged.

```bash
# 🔍 Search for rows tagged as sensitive (Health or Biometric)
grep -i "Yes-" data_inventory.csv
```

**Expected:** You should see the Health Insurance and Biometric Scanner rows listed.

---

## ✔️ Task 4: Validate Lawful Basis and Retention Fields

Write a small Python script to check that no row is missing a lawful basis or retention period.

```bash
# 🐍 Create the validation script
nano validate_ropa.py
```

Use this starter template — complete the `TODOs`:

```python
import csv

def validate_ropa(file_path: str) -> list:
    """
    Check the RoPA CSV file for missing lawful_basis or retention_period.

    Args:
        file_path: Path to the data_inventory.csv file

    Returns:
        List of process_ids that have missing required fields
    """
    missing_rows = []

    # TODO 1: Open the CSV file using open() and csv.DictReader
    # TODO 2: Loop through each row
    # TODO 3: If lawful_basis or retention_period is empty, add process_id to missing_rows
    # TODO 4: Return missing_rows

    pass


if __name__ == "__main__":
    result = validate_ropa("data_inventory.csv")
    if result:
        print("Rows missing required fields:", result)
    else:
        print("All rows have lawful basis and retention period defined.")
```

Run it:

```bash
python3 validate_ropa.py
```

> 💡 **Hint:** Use `csv.DictReader(f)` to read rows as dictionaries, then check `row["lawful_basis"].strip() == ""`.

---

## 📤 Task 5: Generate an Exportable RoPA Report

Create a report generator script:

```bash
# 🐍 Create the report generator script
nano generate_report.py
```

Starter template:

```python
import csv
from datetime import datetime

def generate_ropa_report(input_file: str, output_file: str) -> None:
    """
    Read the data inventory CSV and generate a formatted RoPA report
    (plain text file) for the DPO.

    Args:
        input_file: Path to data_inventory.csv
        output_file: Path to save the report (e.g., ropa_report.txt)
    """
    # TODO 1: Open input_file and read rows with csv.DictReader
    # TODO 2: Open output_file for writing
    # TODO 3: Write a title line and generation date (use datetime.now())
    # TODO 4: For each row, write process_name, data_subject_category,
    #         sensitive_category, lawful_basis, and retention_period
    # TODO 5: Close both files (or use 'with' blocks)

    pass


if __name__ == "__main__":
    generate_ropa_report("data_inventory.csv", "ropa_report.txt")
    print("Report generated: ropa_report.txt")
```

Run the script:

```bash
python3 generate_report.py
```

View your report:

```bash
cat ropa_report.txt
```

---

## ✅ Verification

Confirm your lab is complete by running these checks on the same machine:

```bash
# 1️⃣ Confirm the CSV has at least 6 data rows (plus header)
wc -l data_inventory.csv

# 2️⃣ Confirm sensitive categories are tagged
grep -c "Yes-" data_inventory.csv

# 3️⃣ Confirm validation script runs without errors
python3 validate_ropa.py

# 4️⃣ Confirm the report file exists and has content
ls -la ropa_report.txt
cat ropa_report.txt
```

**Expected outcomes:**
- `data_inventory.csv` contains 6+ processing activities
- At least 2 rows tagged with a sensitive category
- `validate_ropa.py` reports no missing fields (after you complete the TODOs correctly)
- `ropa_report.txt` exists and lists all processing activities clearly

---

## 🔧 Troubleshooting

<details>
<summary>Click to expand common issues and fixes</summary>

| Issue | Fix |
|---|---|
| `"python3: command not found"` | Run `sudo apt install -y python3` |
| CSV columns misaligned | Ensure fields with commas (e.g., `"Name, Email"`) are wrapped in double quotes |
| Script prints nothing | Check indentation; Python is sensitive to spacing |
| `grep` finds nothing | Confirm your sensitive tags exactly match `"Yes-Health"` or `"Yes-Biometric"` (case matters unless using `-i`) |
| Permission denied saving file | Ensure you are working inside `~/gdpr-lab`, not a system folder |

</details>

---

## 🔑 Key Concepts

| Concept | Description |
|---|---|
| RoPA | A structured log of an organization's personal data processing activities |
| Data Subject Categories | Classifying whose data is processed (employees, customers, visitors) |
| Special Category Data | Sensitive data (health, biometric) requiring extra tagging and protection |
| Lawful Basis | The legal justification required for each processing activity under GDPR |
| Retention Period | The documented duration personal data is kept before deletion |
| GDPR Article 30 / GCC PDPL | The regulatory basis requiring organizations to maintain processing records |

---

## 🏁 Conclusion

### 🎉 Key Accomplishments
- Built a basic personal data inventory and Record of Processing Activities (RoPA) using a CSV file and Python scripts
- Enumerated data sources, data subject categories, and processing purposes
- Tagged sensitive data such as health and biometric information
- Validated that each processing activity had a documented lawful basis and retention period
- Generated an exportable text report suitable for a Data Protection Officer

### 💼 Real-World Applications
These skills directly support **GDPR Article 30** and **GCC PDPL** accountability requirements and form a foundational practice for roles such as **Data Privacy Officer** and **Compliance Analyst**, aligning with IAPP **CIPP/E** and **CIPM** certification knowledge areas.

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Education-blue?style=for-the-badge)

</div>
