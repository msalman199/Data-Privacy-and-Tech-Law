# 🔐 Privacy by Design Review with LINDDUN Threat Modeling

> 🛡️ A hands-on privacy engineering lab for analyzing an **ID verification microservice** using **LINDDUN privacy threat modeling**, GDPR principles, GCC data-protection regulations, and Privacy Enhancing Technologies (PETs).

---

## 🎯 Objectives

By completing this lab, you will be able to:

* 🧩 Model an ID verification microservice using a **Data Flow Diagram (DFD)**.
* 🔎 Apply the **LINDDUN privacy threat modeling methodology** systematically.
* 🛡️ Identify privacy threats across processes, data stores, and data flows.
* ⚖️ Map privacy threats to relevant **GDPR Articles 5, 6, 9, 25, 32, and 35**.
* 🌍 Map applicable threats to GCC data-protection requirements.
* 🔐 Select appropriate **Privacy Enhancing Technologies (PETs)**.
* 📊 Prioritize privacy risks using severity ratings.
* 📋 Produce a remediation backlog suitable for privacy architecture and engineering teams.
* 🏗️ Apply **Privacy by Design** principles to system architecture.

---

## 🧠 LINDDUN Framework

LINDDUN is a privacy threat-modeling methodology used to identify threats involving personal data.

| 🔤 Category                | 🔎 Meaning                                                      |
| -------------------------- | --------------------------------------------------------------- |
| 🔗 **L — Linkability**     | Ability to associate multiple data records with the same person |
| 👤 **I — Identifiability** | Ability to identify an individual from data                     |
| 🚫 **N — Non-repudiation** | Ability to associate actions or claims with an individual       |
| 👁️ **D — Detectability**  | Ability to determine whether personal data or a person exists   |
| 📤 **D — Disclosure**      | Unauthorized exposure of personal information                   |
| ❓ **U — Unawareness**      | Individual lacks awareness of data processing                   |
| ⚖️ **N — Non-compliance**  | Processing violates privacy or regulatory requirements          |

---

## 🏗️ Scenario — IDVerify

The lab analyzes a fictional **IDVerify** microservice used by a GCC fintech application for customer onboarding.

### 🔄 System Components

```text
📱 Mobile Client
      │
      ▼
🌐 API Gateway
      │
      ▼
🤖 OCR / Face-Match Service
      │
      ▼
🐘 PostgreSQL
      │
      ├──────────────► 📋 Audit Logging Service
      │
      ▼
🖥️ Admin Dashboard
```

### Components

| Component                 | Function                                                 |
| ------------------------- | -------------------------------------------------------- |
| 📱 Mobile Client          | Uploads ID image and selfie                              |
| 🌐 API Gateway            | Receives and routes requests                             |
| 🤖 OCR/Face-Match Service | Extracts identity information and performs face matching |
| 🐘 PostgreSQL             | Stores extracted PII and verification status             |
| 📋 Audit Logging Service  | Records verification and administrative events           |
| 🖥️ Admin Dashboard       | Allows compliance officers to review flagged cases       |

---

# 🛠️ Technologies & Tools

![Linux](https://img.shields.io/badge/Linux-Lab_Environment-FCC624?style=for-the-badge\&logo=linux\&logoColor=black)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?style=for-the-badge\&logo=git\&logoColor=white)
![Draw.io](https://img.shields.io/badge/Draw.io-Data_Flow_Diagrams-F08705?style=for-the-badge\&logo=diagramsdotnet\&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-Threat_Registers-217346?style=for-the-badge)
![Markdown](https://img.shields.io/badge/Markdown-Documentation-000000?style=for-the-badge\&logo=markdown\&logoColor=white)
![GDPR](https://img.shields.io/badge/GDPR-Privacy_Compliance-8B0000?style=for-the-badge)
![LINDDUN](https://img.shields.io/badge/LINDDUN-Threat_Modeling-6A1B9A?style=for-the-badge)

---

# 📋 Prerequisites

Before starting this lab, you should have:

* 🔐 Knowledge of LINDDUN categories
* ⚖️ Familiarity with GDPR privacy principles
* 🌍 Basic understanding of GCC data-protection regulations
* 🧩 Understanding of Data Flow Diagrams
* 🛡️ Familiarity with threat-modeling terminology
* 🐧 Basic Linux CLI knowledge
* 🔀 Basic Git knowledge

---

# 🚀 Step 1 — Environment Setup

Update the Linux package repository:

```bash
sudo apt update
```

Install Java, Git, and cURL:

```bash
sudo apt install -y default-jre git curl
```

Download draw.io Desktop:

```bash
curl -L -o drawio.AppImage \
https://github.com/jgraph/drawio-desktop/releases/latest/download/drawio-x86_64.AppImage
```

Make it executable:

```bash
chmod +x drawio.AppImage
```

Launch draw.io:

```bash
./drawio.AppImage --no-sandbox &
```

---

# 📁 Step 2 — Create the Lab Structure

Create the working directories:

```bash
mkdir -p ~/linddun-lab/{diagrams,threats,backlog}
```

Move into the project:

```bash
cd ~/linddun-lab
```

Initialize Git:

```bash
git init
```

Expected structure:

```text
linddun-lab/
├── diagrams/
│   ├── idverify_dfd.drawio
│   └── idverify_dfd.png
│
├── threats/
│   ├── linddun_register.csv
│   ├── compliance_mapping.csv
│   └── mitigations.csv
│
└── backlog/
    └── remediation_backlog.md
```

---

# 🧩 Step 3 — Build the Data Flow Diagram

Use draw.io to create the **IDVerify Data Flow Diagram**.

The diagram should contain:

### 📦 Components

* 📱 Mobile Client
* 🌐 API Gateway
* 🤖 OCR/Face-Match Service
* 🐘 PostgreSQL
* 📋 Audit Logging Service
* 🖥️ Admin Dashboard

### 🔐 Trust Boundaries

Include at least two trust boundaries:

```text
📱 Mobile Client
       │
       │ 🔐 Trust Boundary
       ▼
🌐 API Gateway
       │
       │ 🔐 Trust Boundary
       ▼
🤖 Third-Party OCR API
```

### 🏷️ Label Data Flows

Examples:

```text
ID image
Selfie
Extracted PII
Match score
Verification status
Audit event
Admin query
```

### ✅ DFD Requirements

The diagram must contain:

* ≥ 6 elements
* ≥ 7 labeled data flows
* ≥ 2 trust boundaries

Save the source diagram as:

```text
diagrams/idverify_dfd.drawio
```

Export a PNG reference:

```text
diagrams/idverify_dfd.png
```

---

# 🔎 Step 4 — Enumerate LINDDUN Threats

Create:

```bash
nano threats/linddun_register.csv
```

Use the following columns:

```csv
threat_id,dfd_element,linddun_category,threat_description,attacker_capability,affected_data
```

The register should contain **at least 12 distinct threats**.

### 🎯 Coverage Requirements

Threats should cover at least **5 of the 7 LINDDUN categories**.

Special attention should be given to:

* 🤖 Third-party OCR API
* 🐘 PostgreSQL datastore
* 📋 Audit logging
* 🔗 Biometric linkage
* 👁️ API detectability
* ❓ User awareness
* 🚫 Regulatory compliance

---

# 🔗 Example Threat Areas

### 🔗 Linkability

A selfie and identity document could potentially be linked through persistent identifiers.

### 👤 Identifiability

Extracted identity information may directly identify a person.

### 🚫 Non-repudiation

Audit records may create persistent associations between users and actions.

### 👁️ Detectability

Different API response times or error messages could reveal whether an individual exists.

### 📤 Disclosure

Sensitive identity information could be exposed through unauthorized access.

### ❓ Unawareness

Users may not understand that their biometric information is sent to a third-party service.

### ⚖️ Non-compliance

Processing may violate applicable privacy principles or regulatory requirements.

---

# ⚖️ Step 5 — Map Threats to GDPR & PDPL

Create:

```bash
nano threats/compliance_mapping.csv
```

Use:

```csv
threat_id,gdpr_article,gdpr_principle,pdpl_reference,compliance_gap_description
```

### 🇪🇺 GDPR References

Consider relevant provisions including:

* **Article 5** — Principles relating to processing
* **Article 6** — Lawfulness of processing
* **Article 9** — Special categories of personal data
* **Article 25** — Data protection by design and by default
* **Article 32** — Security of processing
* **Article 35** — Data Protection Impact Assessment

### 🧬 Biometric Data

Threats involving biometric information should explicitly consider **GDPR Article 9** where applicable.

Examples include:

```text
Selfie
Face template
Face-match information
Biometric verification result
```

### 🌍 GCC Privacy Regulations

Where applicable, map threats to the relevant provisions of:

* 🇦🇪 UAE Federal Decree-Law No. 45 of 2021
* 🇸🇦 Saudi Personal Data Protection Law (PDPL)
* 🇦🇪 DIFC Data Protection Law

> ⚠️ Regulatory mappings should be validated against the current official legislation and applicable jurisdiction before being used for production compliance decisions.

---

# 🔐 Step 6 — Select Privacy Enhancing Technologies

Create:

```bash
nano threats/mitigations.csv
```

Use:

```csv
threat_id,proposed_pet,implementation_location,residual_risk,implementation_cost(L/M/H)
```

Avoid generic mitigation statements.

Instead, identify a specific PET or architectural control and explain where it is applied.

---

# 🧰 Recommended PETs

### 🔐 Tokenization

Replace direct identifiers with tokens before storing information.

```text
Original PII
     │
     ▼
Tokenization
     │
     ▼
Token
     │
     ▼
Database
```

---

### 📱 On-Device Face Matching

Where technically and legally appropriate, perform biometric comparison on the client device to reduce unnecessary transmission.

```text
ID + Selfie
     │
     ▼
📱 Device
     │
     ▼
Face Matching
     │
     ▼
Match Result
```

This can reduce the amount of sensitive information sent to external services.

---

### 📊 Differential Privacy

Apply differential privacy to aggregated analytics rather than exposing raw personal records.

```text
Raw Data
   ↓
Aggregation
   ↓
Differential Privacy
   ↓
Analytics
```

---

### 🔐 Secure Enclaves

Consider confidential-computing environments for sensitive processing where appropriate.

---

### 🔒 Homomorphic Encryption

For suitable workloads, consider privacy-preserving computation where data remains protected during processing.

---

### 🎟️ Unlinkable Identifiers

Use short-lived or per-session identifiers instead of persistent identifiers where persistent linkage is unnecessary.

---

### 👥 K-Anonymity

Consider k-anonymity or related privacy techniques for appropriate administrative exports and aggregate datasets.

---

# 📊 Step 7 — Create the Remediation Backlog

Create:

```bash
nano backlog/remediation_backlog.md
```

Use the following structure:

```markdown
| ID | LINDDUN Category | Severity | GDPR/PDPL Ref | Mitigation Summary | Owner | Target Sprint |
|---|---|---|---|---|---|---|
```

The backlog must contain:

* At least 12 entries
* One entry for every identified threat
* Severity rating
* Compliance references
* Mitigation summary
* Responsible role
* Target sprint

---

# 🚦 Severity Model

Use an **Impact × Likelihood** scoring approach.

```text
Risk Score = Impact × Likelihood
```

Suggested scale:

| Score | Severity    |
| ----: | ----------- |
| 16–25 | 🔴 Critical |
| 10–15 | 🟠 High     |
|   5–9 | 🟡 Medium   |
|   1–4 | 🟢 Low      |

### Example

```text
Impact:     5
Likelihood: 4
----------------
Risk Score: 20
Severity:   Critical
```

Sort the remediation backlog from highest to lowest severity.

---

# 🧑‍💼 Step 8 — Executive Privacy Summary

Add an executive summary at the beginning of the remediation backlog.

The summary should identify:

### 🔴 Top Systemic Issues

Examples:

1. 🤖 Third-party OCR processing creates a significant external trust boundary.
2. 🧬 Biometric information creates elevated privacy and regulatory risk.
3. 📋 Persistent identifiers and audit records may increase linkability.

The summary should explain the overall privacy posture and identify the highest-priority architectural issues.

---

# 🔍 Step 9 — Verification

Move into the lab directory:

```bash
cd ~/linddun-lab
```

Verify the DFD:

```bash
test -f diagrams/idverify_dfd.drawio && \
echo "DFD: OK" || echo "DFD: MISSING"
```

Check the LINDDUN register:

```bash
wc -l threats/linddun_register.csv
```

Expected:

```text
>= 13
```

This represents:

```text
1 header + 12 threats
```

Check LINDDUN categories:

```bash
cut -d, -f3 threats/linddun_register.csv | sort -u
```

Confirm that at least **5 categories** are represented.

---

# 🔗 Step 10 — Check Threat Mapping

Check compliance mapping:

```bash
wc -l threats/compliance_mapping.csv
```

Check mitigations:

```bash
wc -l threats/mitigations.csv
```

Check remediation entries:

```bash
grep -c "Critical\|High\|Med\|Low" \
backlog/remediation_backlog.md
```

---

# 🔎 Step 11 — Check for Orphan Threats

Every threat must have:

```text
Threat Register
       │
       ├────► Compliance Mapping
       │
       └────► Mitigation
```

Run:

```bash
comm -3 \
<(cut -d, -f1 threats/linddun_register.csv | sort) \
<(cut -d, -f1 threats/mitigations.csv | sort)
```

Ideally, the command should return no unexpected threat IDs.

Perform the same consistency check against `compliance_mapping.csv`.

---

# ✅ Manual Review Checklist

Before completing the lab, verify:

* [ ] 📊 DFD contains at least 6 elements.
* [ ] 🔀 DFD contains at least 7 labeled flows.
* [ ] 🔐 DFD contains at least 2 trust boundaries.
* [ ] 🔎 At least 12 LINDDUN threats are documented.
* [ ] 🧩 At least 5 LINDDUN categories are represented.
* [ ] 🤖 Third-party OCR API is addressed.
* [ ] 🐘 PostgreSQL datastore is addressed.
* [ ] 📋 Audit logging is addressed.
* [ ] 🧬 Biometric threats are identified.
* [ ] ⚖️ GDPR references are mapped.
* [ ] 🌍 Applicable PDPL references are mapped.
* [ ] 🔐 Every threat has a mitigation.
* [ ] 📊 Every threat has a severity rating.
* [ ] 🧑‍💼 Every backlog item has an owner.
* [ ] 🏃 Every backlog item has a target sprint.
* [ ] 🔗 No orphan threat IDs exist.

---

# 📁 Final Repository Structure

```text
linddun-lab/
│
├── 📊 diagrams/
│   ├── idverify_dfd.drawio
│   └── idverify_dfd.png
│
├── 🔐 threats/
│   ├── linddun_register.csv
│   ├── compliance_mapping.csv
│   └── mitigations.csv
│
├── 📋 backlog/
│   └── remediation_backlog.md
│
└── 📖 README.md
```

---

# 🔀 Step 12 — Commit the Project

Stage all files:

```bash
git add -A
```

Create the commit:

```bash
git commit -m \
"LINDDUN privacy threat model for IDVerify service"
```

Verify the commit:

```bash
git log --oneline -1
```

---

# 🏗️ End-to-End Privacy Engineering Workflow

```text
                 🏦 IDVerify System
                         │
                         ▼
                  📊 Build DFD
                         │
                         ▼
                 🔐 Identify
               Trust Boundaries
                         │
                         ▼
                🔎 Apply LINDDUN
                         │
                         ▼
                📋 Threat Register
                         │
                         ▼
              ⚖️ GDPR / PDPL Mapping
                         │
                         ▼
                 🛡️ Select PETs
                         │
                         ▼
               🚦 Risk Assessment
                         │
                         ▼
               📋 Remediation Backlog
                         │
                         ▼
                  🚀 Engineering
                    Execution
```

---

# 📚 Key Privacy Engineering Concepts

| 🔐 Concept                | 📝 Implementation                            |
| ------------------------- | -------------------------------------------- |
| LINDDUN                   | Privacy threat identification                |
| Privacy by Design         | Privacy controls embedded into architecture  |
| Data Minimization         | Reduce unnecessary personal-data processing  |
| Pseudonymization          | Replace direct identifiers                   |
| Tokenization              | Protect stored identifiers                   |
| Unlinkability             | Reduce persistent data associations          |
| Differential Privacy      | Protect aggregate analytics                  |
| Secure Processing         | Reduce exposure during sensitive computation |
| Trust Boundaries          | Identify external processing risks           |
| DPIA/PIA                  | Assess privacy risks and controls            |
| Risk-Based Prioritization | Prioritize remediation activities            |

---

# 🎓 Learning Outcomes

After completing this lab, you should be able to:

* ✅ Build privacy-focused Data Flow Diagrams.
* ✅ Apply all seven LINDDUN categories.
* ✅ Identify privacy threats in distributed systems.
* ✅ Analyze third-party data-processing risks.
* ✅ Identify risks involving biometric information.
* ✅ Map technical risks to privacy regulations.
* ✅ Select appropriate Privacy Enhancing Technologies.
* ✅ Build a severity-based privacy remediation backlog.
* ✅ Apply Privacy by Design principles.
* ✅ Communicate privacy risks to engineering and architecture teams.

---

# 💼 Professional Relevance

This project provides practical experience relevant to:

* 🔐 Privacy Engineering
* 🏗️ Security Architecture
* 🛡️ Cybersecurity
* ⚖️ Governance, Risk & Compliance
* 📊 Privacy Impact Assessments
* 🧑‍💻 Software Architecture
* ☁️ Cloud Security
* 📋 Data Protection
* 🏢 Enterprise Privacy Architecture

---

# 🏆 Final Result

The completed project demonstrates an end-to-end **Privacy by Design review**:

```text
📊 DFD
  ↓
🔎 LINDDUN Threat Modeling
  ↓
⚖️ GDPR / PDPL Analysis
  ↓
🔐 Privacy Enhancing Technologies
  ↓
🚦 Risk Scoring
  ↓
📋 Remediation Backlog
  ↓
🏗️ Privacy-Aware Architecture
```

---

## 👨‍💻 Author

**Hafiz Muhammad Salman**

☁️ Cloud DevOps Engineer | 🐧 Linux Administrator

---

## ⭐ Conclusion

This lab demonstrates how **LINDDUN threat modeling** can be integrated into a real-world Privacy by Design review.

The workflow connects:

> **📊 Data Flow Modeling → 🔐 LINDDUN → ⚖️ Privacy Compliance → 🛡️ PETs → 🚦 Risk Assessment → 📋 Remediation**

It provides practical experience in translating privacy risks into **technical controls, regulatory mappings, and actionable engineering tasks**.

**🔐 Model Privacy Risks • 🛡️ Engineer Privacy Controls • ⚖️ Protect Personal Data • 🚀 Build Secure Systems**
