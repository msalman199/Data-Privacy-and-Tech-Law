<div align="center">

# 🔒 Anonymization with k-Anonymity Using ARX Toolkit

![ARX](https://img.shields.io/badge/ARX-Data%20Anonymization-2E8B57?style=for-the-badge)
![Java](https://img.shields.io/badge/Java-JDK%2011%2B-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Privacy](https://img.shields.io/badge/Privacy-k--Anonymity-6A5ACD?style=for-the-badge)
![GDPR](https://img.shields.io/badge/Compliance-GDPR%20%7C%20GCC%20PDPL-003399?style=for-the-badge)
![Linux](https://img.shields.io/badge/Linux-Ubuntu%2022.04-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**A hands-on lab in de-identifying healthcare data using k-anonymity, l-diversity, and t-closeness**

</div>

---

## 📑 Table of Contents

- [🎯 Learning Objectives](#-learning-objectives)
- [✅ Prerequisites](#-prerequisites)
- [🖥️ Lab Environment](#️-lab-environment)
- [⚙️ Environment Setup](#️-environment-setup)
- [🧩 Task 1: Dataset Preparation and Import](#-task-1-dataset-preparation-and-import)
- [🏗️ Task 2: Attribute Configuration and Hierarchy Design](#️-task-2-attribute-configuration-and-hierarchy-design)
- [🛡️ Task 3: Apply Privacy Models](#️-task-3-apply-privacy-models)
- [📄 Task 4: Export and Compliance Documentation](#-task-4-export-and-compliance-documentation)
- [🔍 Verification](#-verification)
- [📚 Key Concepts](#-key-concepts)
- [🏁 Conclusion](#-conclusion)

---

## 🎯 Learning Objectives

| # | Objective |
|---|-----------|
| 1 | Install and configure the ARX Data Anonymization Tool on Linux |
| 2 | Model quasi-identifiers, sensitive attributes, and hierarchies for a healthcare dataset |
| 3 | Apply k-anonymity (k=5), l-diversity, and t-closeness privacy models |
| 4 | Evaluate utility loss and re-identification risk trade-offs |
| 5 | Produce a compliance-ready anonymization report referencing GDPR Art. 4(5)/Recital 26 and GCC PDPL de-identification provisions |

## ✅ Prerequisites

| Area | Requirement |
|------|-------------|
| 🔐 Privacy Models | Working knowledge of k-anonymity, l-diversity, t-closeness, and quasi-identifier concepts |
| ☕ Java Deployment | Familiarity with Java-based desktop application deployment |
| 🐧 Linux Access | Comfortable with Linux CLI, X11/VNC forwarding, or desktop GUI access |
| 📊 Data Structures | Basic understanding of CSV data structures and generalization hierarchies |
| 📜 Legal Context | Prior exposure to GDPR/PDPL anonymization vs. pseudonymization distinctions |

## 🖥️ Lab Environment

> 💻 **Provided by Al Nafi:** A single Linux machine (Ubuntu 22.04 LTS or similar) via **Start Lab**, with GUI desktop access.

---

## ⚙️ Environment Setup

**🔧 Step 1 — Verify Java (ARX requires JDK 11+)**

```bash
# ☕ Check for an existing JDK, install OpenJDK 17 if missing
java -version || sudo apt update && sudo apt install -y openjdk-17-jdk
```

**🔧 Step 2 — Verify GUI availability**

```bash
# 🖥️ Confirm an X display is available for the ARX GUI
echo $DISPLAY
```

**🔧 Step 3 — Download and launch ARX**

```bash
# 📥 Fetch the latest open-source ARX build (no cloud dependency)
wget https://arx.deidentifier.org/wp-content/uploads/2024/latest/arx-*-linux.gtk.x86_64.zip -O arx.zip

# 📦 Unpack into a dedicated directory
mkdir -p ~/arx && unzip arx.zip -d ~/arx

# ▶️ Launch the ARX GUI
cd ~/arx && ./arx
```

> ⚠️ **Troubleshooting:** If the GUI fails to launch, verify `libwebkit2gtk` and X11 libraries are installed via `apt`.

---

## 🧩 Task 1: Dataset Preparation and Import

- 🧬 Generate or source a synthetic healthcare dataset (**minimum 500 records**) with fields: `patient_id`, `zipcode`, `age`, `gender`, `nationality`, `diagnosis`, `admission_date`
- 🗑️ Remove direct identifiers (name, national ID, phone) — retain only quasi-identifiers (QIs) and one sensitive attribute (`diagnosis`)
- 💾 Save as `patients.csv` (UTF-8, comma-delimited)
- 📂 In ARX: **File > New Project > Import Data > CSV**, map data types per column (String, Integer, Date)

> 🧠 **Design decision:** Justify which fields qualify as QIs vs. sensitive attributes vs. identifiers to remove entirely, based on linkage-attack feasibility (e.g., zipcode + age + gender re-identification risk per Sweeney's model).

---

## 🏗️ Task 2: Attribute Configuration and Hierarchy Design

- 🏷️ Assign attribute types in ARX's **Configuration** tab: Quasi-identifying, Sensitive, Identifying, Insensitive
- 🌳 Build generalization hierarchies for each QI:
  - **zipcode** — masking hierarchy (5-digit → 3-digit → region)
  - **age** — interval hierarchy (exact → 5-yr bands → decade bands)
  - **nationality** — taxonomy-based hierarchy (country → GCC/non-GCC → region)
- 🛠️ Use ARX's **Hierarchy Builder** (interval/order-based) rather than manual CSV hierarchies where possible

> ⚖️ **Trade-off to evaluate:** Coarser hierarchies reduce re-identification risk but increase information loss — document your rationale for hierarchy granularity choices.

---

## 🛡️ Task 3: Apply Privacy Models

**🔧 Configure in the Privacy Models tab:**

| Model | Parameter |
|-------|-----------|
| k-Anonymity | k = 5 |
| l-Diversity | Distinct l-diversity on `diagnosis`, l = 3 |
| t-Closeness | Earth Mover's Distance (EMD), t = 0.2, on `diagnosis` |

**▶️ Execute anonymization:**

- 🚧 Set suppression limit (e.g., max 5% record suppression)
- ⚙️ Run **Anonymize** and review the solution space (search metric: Loss, or Monotonic Height)
- ⚖️ Compare at least two transformation nodes from the lattice (different generalization levels) using ARX's risk/utility visualization panel

> 📊 **Required analysis:**
> - Screenshot or export the risk analysis (Prosecutor, Journalist, Marketer re-identification risk models)
> - Quantify utility loss using ARX's Discernibility or Loss Metric
> - Identify the Pareto-optimal transformation balancing k=5/l=3/t=0.2 against information loss

---

## 📄 Task 4: Export and Compliance Documentation

- 📤 Export anonymized dataset: **File > Export Data** as `patients_anonymized.csv`
- 🗂️ Export the anonymization configuration/project file for auditability
- 📝 Produce a short compliance memo (`report.md`) covering:
  - Chosen QIs/sensitive attributes and justification
  - Achieved k, l, t values and residual re-identification risk (%)
  - Mapping to GDPR Recital 26 (anonymous data is out of scope) vs. PDPL de-identification/anonymization definitions (KSA PDPL Art. 1, UAE PDPL) — argue whether output qualifies as "anonymous" or remains "pseudonymized"
  - Recommended data retention/access controls for the anonymized dataset

---

## 🔍 Verification

Confirm lab completion on the same machine:

```bash
# 📁 Confirm exported files exist
ls -la ~/arx_project/patients_anonymized.csv ~/arx_project/*.deid ~/arx_project/report.md

# 🔢 Validate row count matches (minus suppressed records)
wc -l patients.csv patients_anonymized.csv
```

- [ ] In ARX, reopen the exported project and confirm the risk panel shows highest re-identification risk ≤ 1/k (20% for k=5)
- [ ] `report.md` explicitly states the final k, l, t values achieved and the legal basis conclusion
- [ ] Spot-check 5 random rows in `patients_anonymized.csv` to confirm no direct identifiers remain and QIs are properly generalized/suppressed

---

## 📚 Key Concepts

| Concept | Description |
|---------|-------------|
| **k-Anonymity** | Each record is indistinguishable from at least k−1 others on its quasi-identifiers |
| **l-Diversity** | Ensures each equivalence class contains at least l well-represented sensitive-attribute values |
| **t-Closeness** | Bounds the distance between the sensitive-attribute distribution in an equivalence class and the overall dataset distribution |
| **Quasi-Identifiers (QIs)** | Attributes that, in combination, can re-identify an individual (e.g., zipcode + age + gender) |
| **Generalization Hierarchy** | A structured mapping from specific values to progressively broader categories, used to reduce re-identification risk |
| **Re-identification Risk Models** | Prosecutor, Journalist, and Marketer models — each assumes a different attacker capability/motivation |
| **Discernibility / Loss Metric** | Quantifies utility loss introduced by generalization and suppression |
| **GDPR Recital 26 vs. GCC PDPL** | Distinguishes truly anonymous data (out of GDPR scope) from pseudonymized data (still regulated) |

---

## 🏁 Conclusion

In this lab, you deployed ARX on a Linux environment and applied a layered anonymization strategy — k-anonymity, l-diversity, and t-closeness — to a synthetic healthcare dataset. You made independent architectural decisions on quasi-identifier selection, hierarchy design, and privacy model parameterization, then evaluated the inherent trade-off between re-identification risk and data utility using ARX's risk analysis and information loss metrics. Finally, you produced compliance documentation mapping technical outcomes to GDPR and GCC PDPL anonymization standards.

### 🏆 Key Accomplishments

- ✅ Deployed and configured the ARX Data Anonymization Tool on Linux
- ✅ Designed generalization hierarchies for zipcode, age, and nationality
- ✅ Applied k=5 anonymity, l=3 diversity, and t=0.2 closeness to a healthcare dataset
- ✅ Evaluated re-identification risk vs. utility loss trade-offs across transformation nodes
- ✅ Produced a defensible GDPR/GCC PDPL compliance memo

### 🌍 Real-World Applications

- 🏥 Preparing healthcare datasets for lawful secondary research use
- 📋 Supporting IAPP CIPT certification and Privacy Engineering career paths
- ⚖️ Demonstrating anonymization vs. pseudonymization distinctions for regulators and auditors
- 🔐 Building repeatable de-identification pipelines for cross-jurisdictional (GDPR + GCC PDPL) compliance

---

<div align="center">

![Al Nafi](https://img.shields.io/badge/Al%20Nafi-Cybersecurity%20Training-1E90FF?style=for-the-badge)

</div>
