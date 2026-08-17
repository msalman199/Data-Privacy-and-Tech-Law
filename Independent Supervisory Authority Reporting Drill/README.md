<div align="center">

# 🏛️ Independent Supervisory Authority Reporting Drill

![Regulatory](https://img.shields.io/badge/Regulatory-Oversight-8B0000?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Web%20App-000000?style=for-the-badge&logo=flask&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandoc](https://img.shields.io/badge/Pandoc-PDF%20Report-1A5276?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Terminal-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**Simulating a data protection authority's complaint-to-oversight-report lifecycle**

</div>

---

## 📑 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [⚙️ Environment Setup](#️-environment-setup)
- [📝 Task 1: Draft a Complaint Intake Form (Local Webapp)](#-task-1-draft-a-complaint-intake-form-local-webapp)
- [🔍 Task 2: Investigate the Complaint Using Log Evidence](#-task-2-investigate-the-complaint-using-log-evidence)
- [📄 Task 3: Issue a Remedial Action Decision Document](#-task-3-issue-a-remedial-action-decision-document)
- [📊 Task 4: Compile Annual Statistics in a Linux Notebook](#-task-4-compile-annual-statistics-in-a-linux-notebook)
- [📑 Task 5: Publish an Oversight Report PDF](#-task-5-publish-an-oversight-report-pdf)
- [🔍 Verification](#-verification)
- [📚 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | Build a simple local web form to intake data protection complaints |
| 2 | Investigate a simulated complaint using log analysis techniques |
| 3 | Draft a formal remedial action decision document |
| 4 | Compile annual data protection statistics using a Jupyter notebook |
| 5 | Generate a publishable oversight report in PDF format |

## ✅ Prerequisites

| Area | Requirement |
|------|-------------|
| 🐍 Python/Flask | Basic Python (Flask) and command-line familiarity |
| 🔐 Privacy Concepts | Understanding of data protection concepts (breach notification, complaint handling, DPIAs) |
| 📄 Log Structure | Basic knowledge of log file structure (timestamps, IP addresses, status codes) |
| 📓 Notebooks | Familiarity with Markdown/Jupyter notebooks |

## 🖥️ Lab Environment

> 💻 **Provided by Al Nafi:** A single Linux machine via **Start Lab**.

---

## ⚙️ Environment Setup

```bash
# 📦 Install required system packages
sudo apt update
sudo apt install -y python3-pip python3-venv pandoc texlive-latex-base

# 🐍 Create and activate a virtual environment
python3 -m venv sa_lab_env
source sa_lab_env/bin/activate

# 📦 Install Python packages
pip install flask pandas matplotlib jupyter nbconvert

# 📁 Create lab working directories
mkdir -p ~/sa_drill/{app,logs,reports,notebook}
cd ~/sa_drill
```

Download the simulated log file (or create it manually if offline):

```bash
# 📄 Generate the simulated access log
cat << 'EOF' > logs/access.log
2024-03-01 09:12:33 192.168.1.10 GET /user/4521/export STATUS=200
2024-03-01 09:14:02 192.168.1.10 GET /user/4521/export STATUS=200
2024-03-01 09:14:45 192.168.1.55 GET /user/4521/profile STATUS=403
2024-03-02 11:20:10 192.168.1.10 POST /admin/bulk_export STATUS=200
2024-03-02 11:21:00 192.168.1.10 GET /user/9981/export STATUS=200
EOF
```

---

## 📝 Task 1: Draft a Complaint Intake Form (Local Webapp)

> 🧭 Create a minimal Flask app that captures complaint details (complainant, data subject, nature of complaint, date).

```python
# app/intake_app.py
from flask import Flask, request, render_template_string
import json, datetime

app = Flask(__name__)
COMPLAINTS_FILE = "complaints.json"

FORM_HTML = """
<form method="POST">
  Complainant Name: <input name="name"><br>
  Email: <input name="email"><br>
  Nature of Complaint: <textarea name="nature"></textarea><br>
  Data Subject ID: <input name="subject_id"><br>
  <input type="submit">
</form>
"""

@app.route("/", methods=["GET", "POST"])
def intake():
    if request.method == "POST":
        # TODO: Build a dict with form fields + a timestamp + a unique complaint ID
        # TODO: Append the dict to COMPLAINTS_FILE (create file if missing)
        # TODO: Return a confirmation message showing the complaint ID
        pass
    return FORM_HTML

if __name__ == "__main__":
    app.run(port=5000)
```

Run it and submit at least one test complaint via browser or `curl`:

```bash
# ▶️ Launch the intake app
python3 app/intake_app.py &

# 📨 Submit a test complaint
curl -X POST -d "name=Jane Doe&email=jane@example.com&nature=Unauthorized export of my data&subject_id=4521" http://127.0.0.1:5000/
```

Verify `complaints.json` was created with your submitted entry.

---

## 🔍 Task 2: Investigate the Complaint Using Log Evidence

> 🧭 Write a Python script to parse `logs/access.log` and correlate entries with the `subject_id` from the complaint.

```python
# app/investigate.py
import re

LOG_FILE = "logs/access.log"

def parse_logs(subject_id: str) -> list:
    """
    Search log file for entries referencing the given subject_id.

    Args:
        subject_id: The data subject ID under investigation

    Returns:
        List of matching log line dicts (timestamp, ip, action, status)
    """
    # TODO: Open LOG_FILE and read lines
    # TODO: Use regex to extract timestamp, IP, HTTP method+path, status
    # TODO: Filter lines containing subject_id
    # TODO: Return list of structured dicts
    pass

if __name__ == "__main__":
    results = parse_logs("4521")
    for r in results:
        print(r)
```

Run the script:

```bash
python3 app/investigate.py
```

> 🧠 **Analysis:** Identify whether the access pattern indicates unauthorized bulk export (hint: check repeated `GET /export` and any correlated `/admin/bulk_export` calls from the same IP).

---

## 📄 Task 3: Issue a Remedial Action Decision Document

> 🧭 Create a Markdown decision document summarizing findings and required remedial actions, mirroring formats used by SDAIA/ICO/UAE Data Office.

```bash
# 📄 Generate the decision document skeleton
cat << 'EOF' > reports/decision_2024_001.md
# Regulatory Decision Notice

**Case Reference:** DPA-2024-001
**Date Issued:** $(date +%Y-%m-%d)
**Subject Organization:** [TODO: Insert org name]

## Summary of Complaint
[TODO: Summarize complainant's allegation]

## Findings
[TODO: Insert findings from log investigation - cite timestamps/IPs]

## Legal Basis
[TODO: Reference relevant article, e.g., PDPL Article X / UK GDPR Art. 5]

## Remedial Actions Required
1. [TODO]
2. [TODO]

## Compliance Deadline
[TODO: Insert date, e.g., 30 days from issuance]
EOF
```

Fill in all `TODO` placeholders based on your Task 2 findings.

---

## 📊 Task 4: Compile Annual Statistics in a Linux Notebook

> 🧭 Launch Jupyter and build a notebook that aggregates complaint statistics.

```bash
# ▶️ Launch Jupyter Notebook
jupyter notebook --no-browser --port=8888 --ip=0.0.0.0 &
```

In `notebook/annual_stats.ipynb`, implement:

```python
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_complaints(path: str) -> pd.DataFrame:
    """
    Load complaints.json into a pandas DataFrame.
    """
    # TODO: Read JSON lines/array into DataFrame
    pass

def summarize_stats(df: pd.DataFrame) -> dict:
    """
    Compute total complaints, complaints by nature category,
    and average resolution time (if resolved_date exists).
    """
    # TODO: Compute counts and groupby summaries
    # TODO: Return a dict of summary statistics
    pass

# TODO: Call functions, print summary, and plot a bar chart
# of complaints by category using matplotlib
```

Save at least one chart as `notebook/complaints_chart.png`.

---

## 📑 Task 5: Publish an Oversight Report PDF

> 🧭 Combine the decision document and statistics into a single PDF report using `pandoc`.

```bash
# 📄 Assemble the combined report source
cat reports/decision_2024_001.md > reports/annual_oversight_report.md
echo "\n## Annual Statistics\n" >> reports/annual_oversight_report.md
echo "![Complaints Chart](../notebook/complaints_chart.png)" >> reports/annual_oversight_report.md

# 📑 Render to PDF
pandoc reports/annual_oversight_report.md -o reports/annual_oversight_report.pdf
```

Confirm the PDF was generated and contains both narrative and chart.

---

## 🔍 Verification

Run these checks on your machine to confirm task completion:

```bash
# Task 1
ls app/complaints.json && cat app/complaints.json

# Task 2
python3 app/investigate.py | grep "4521"

# Task 3
grep -c "TODO" reports/decision_2024_001.md   # should return 0 after completion

# Task 4
ls notebook/complaints_chart.png

# Task 5
ls -lh reports/annual_oversight_report.pdf
```

**Expected outcome:** All commands should return valid file contents/paths with no errors and no remaining TODO placeholders.

<details>
<summary>⚠️ Troubleshooting</summary>

- **Flask port in use:** kill existing process with `pkill -f intake_app.py`
- **Pandoc PDF fails:** ensure `texlive-latex-base` installed; retry with `--pdf-engine=xelatex` if needed
- **Jupyter not accessible:** check firewall/port 8888 is open on the lab VM
- **Regex not matching logs:** print raw lines first to confirm log format before applying regex

</details>

---

## 📚 Key Concepts

| Concept | Description |
|---------|-------------|
| **Complaint Intake** | The formal process of capturing and logging a data subject's complaint with a unique reference |
| **Log-Based Investigation** | Correlating access-log evidence (timestamps, IPs, endpoints) against a complaint to establish facts |
| **Regulatory Decision Notice** | A formal document recording findings, legal basis, and required remedial actions |
| **Remedial Actions & Compliance Deadline** | Binding corrective steps issued to an organization with a fixed timeframe for resolution |
| **Annual Statistics Reporting** | Aggregating complaint volume and categories to support transparency and oversight |
| **Oversight Report** | A consolidated, publishable document combining narrative findings and statistical summaries |
| **Regulatory Analogues** | SDAIA, ICO, and UAE Data Office decision/reporting formats used as real-world references |

---

## 🏁 Conclusion

In this lab, you simulated the full lifecycle of a data protection authority's complaint handling and annual reporting workflow. You built a complaint intake webapp, investigated evidence using log analysis, drafted a formal regulatory decision notice, compiled statistical summaries in a notebook, and published a consolidated oversight report as a PDF.

### 🏆 Key Accomplishments

- ✅ Built a Flask-based complaint intake webapp with persistent JSON storage
- ✅ Investigated a simulated complaint using regex-based log correlation
- ✅ Drafted a formal regulatory decision notice with findings and remedial actions
- ✅ Compiled annual complaint statistics in a Jupyter notebook
- ✅ Published a consolidated oversight report as a PDF via Pandoc

### 🌍 Real-World Applications

- 🏛️ Mirrors real-world responsibilities of Regulatory Liaisons and DPOs operating under SDAIA, ICO, and UAE Data Office frameworks
- 🔍 Building evidence-based investigation workflows for data protection complaints
- 📊 Producing transparency reporting for regulatory and board audiences
- 🎓 Aligns with IAPP CIPM competency areas in program governance and incident response reporting

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Training-1E90FF?style=for-the-badge)

</div>
