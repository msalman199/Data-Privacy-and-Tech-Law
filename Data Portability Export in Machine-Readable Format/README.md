# 🔐 Data Portability Export in Machine-Readable Format

<p align="center">
  <img src="https://img.shields.io/badge/GDPR-Article%2020-0052CC?style=for-the-badge&logo=gdpr&logoColor=white" alt="GDPR">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/JSON-Machine%20Readable-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON">
  <img src="https://img.shields.io/badge/CSV-Export-217346?style=for-the-badge" alt="CSV">
  <img src="https://img.shields.io/badge/GPG-Encryption%20%26%20Signing-4A4A4A?style=for-the-badge&logo=gnuprivacyguard&logoColor=white" alt="GPG">
  <img src="https://img.shields.io/badge/SFTP-Secure%20Transfer-2E8B57?style=for-the-badge" alt="SFTP">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu">
  <img src="https://img.shields.io/badge/SQLite-Like%20Sample%20Data-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/JSONSchema-Validation-CC2927?style=for-the-badge" alt="JSON Schema">
  <img src="https://img.shields.io/badge/OpenSSH-SFTP-000000?style=for-the-badge&logo=openssh&logoColor=white" alt="OpenSSH">
  <img src="https://img.shields.io/badge/Privacy-Data%20Protection-6A1B9A?style=for-the-badge" alt="Privacy">
</p>

---

## 📌 Project Overview

This hands-on lab demonstrates how to implement a simplified **GDPR Article 20 Data Portability** workflow.

The project extracts user-provided data from a sample record, generates machine-readable **JSON and CSV** files, digitally signs the JSON export using **GPG**, transfers the files through **SFTP**, and validates the JSON export against a defined **JSON Schema**.

### 🔄 End-to-End Workflow

```text
                  ┌──────────────────────┐
                  │   Sample User Data   │
                  │      Python Dict     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Portable Data Filter │
                  │     Python Script    │
                  └──────────┬───────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌────────────────┐      ┌────────────────┐
        │   export.json  │      │   export.csv   │
        └───────┬────────┘      └────────────────┘
                │
                ▼
        ┌────────────────┐
        │ GPG Signature  │
        │ export.json.sig│
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │  Local SFTP    │
        │ Secure Transfer│
        └───────┬────────┘
                │
                ▼
        ┌────────────────┐
        │ JSON Schema    │
        │   Validation   │
        └────────────────┘
```

---

# 🎯 Objectives

By completing this lab, you will be able to:

* 🔍 Identify data that qualifies as portable under **GDPR Article 20**
* 🐍 Build a Python data-export utility
* 📄 Export user data into **JSON**
* 📊 Export user data into **CSV**
* 🔐 Create a GPG digital signature
* ✅ Verify export integrity using GPG
* 🔄 Transfer exported data using local **SFTP**
* 📋 Validate JSON against a JSON Schema
* 🛡️ Prevent internally derived information from being included in the export
* 🧪 Perform end-to-end verification of a privacy-oriented data export workflow

---

# 🧰 Technology Stack

| Technology          | Purpose                                    |
| ------------------- | ------------------------------------------ |
| 🐍 Python 3         | Data extraction and export                 |
| 📄 JSON             | Machine-readable data format               |
| 📊 CSV              | Tabular data export                        |
| 🔐 GPG              | Digital signing and integrity verification |
| 🔄 SFTP             | Secure file transfer                       |
| 🧩 OpenSSH          | Local SFTP server                          |
| 📋 JSON Schema      | Export validation                          |
| 🐧 Linux            | Lab environment                            |
| 🛡️ GDPR Article 20 | Data portability concept                   |

---

# 📋 Prerequisites

Before starting, make sure you have:

* Basic Python knowledge
* Basic Linux command-line knowledge
* Familiarity with files and directories
* No previous cryptography experience required

### ⏱️ Estimated Duration

**45–60 minutes**

---

# 🖥️ Environment Setup

All activities are performed locally on a Linux machine.

## 🚀 Step 1 — Open the Terminal

Open a terminal on your lab machine.

```bash
sudo apt update
```

### ✨ Technology

![Linux](https://img.shields.io/badge/Linux-Environment-E95420?style=flat-square\&logo=linux\&logoColor=white)

---

## 📦 Step 2 — Install Required Packages

```bash
sudo apt install -y python3 python3-pip gnupg openssh-server
```

Install the JSON Schema library:

```bash
pip3 install jsonschema
```

### 🔍 Verify Installation

```bash
python3 --version
gpg --version
ssh -V
```

### ✨ Technology

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square\&logo=python\&logoColor=white)
![GPG](https://img.shields.io/badge/GPG-Security-4A4A4A?style=flat-square)
![OpenSSH](https://img.shields.io/badge/OpenSSH-SFTP-000000?style=flat-square\&logo=openssh\&logoColor=white)

---

## 📁 Step 3 — Create the Project Directory

```bash
mkdir ~/data-portability-lab
cd ~/data-portability-lab
```

Verify:

```bash
pwd
```

Expected location:

```text
/home/<your-user>/data-portability-lab
```

---

# 🧩 Task 1 — Identify Portable Fields

## 🎯 Objective

The first task is to separate:

* ✅ Data provided by the user
* ❌ Data internally derived or created by the organization

Under the simplified model used in this lab, the portable fields are:

```text
full_name
email
phone
signup_date
preferences
```

The following are treated as non-portable for this exercise:

```text
internal_risk_score
admin_notes
```

> ⚠️ **Important:** GDPR Article 20 has specific legal scope and conditions. This lab is an educational implementation and does not constitute legal advice.

---

## 📝 Step 1 — Create `sample_data.py`

```bash
nano sample_data.py
```

Add:

```python
# sample_data.py
# This simulates a row from a user database.

USER_RECORD = {
    "user_id": "U1001",
    "full_name": "Aisha Al Farsi",
    "email": "aisha@example.com",
    "phone": "+971500000000",
    "signup_date": "2023-01-15",
    "preferences": {
        "newsletter": True
    },
    "internal_risk_score": 0.82,
    "admin_notes": "VIP customer"
}
```

Save:

```text
CTRL + O
ENTER
CTRL + X
```

### ✨ Technology

![Python](https://img.shields.io/badge/Python-Data%20Model-3776AB?style=flat-square\&logo=python\&logoColor=white)

---

## 🔎 Step 2 — Review the Data

```bash
cat sample_data.py
```

You should see both portable and internal fields.

### 📌 Data Classification

| Field                 | Classification         |
| --------------------- | ---------------------- |
| `user_id`             | ✅ Exported in this lab |
| `full_name`           | ✅ Portable             |
| `email`               | ✅ Portable             |
| `phone`               | ✅ Portable             |
| `signup_date`         | ✅ Portable             |
| `preferences`         | ✅ Portable             |
| `internal_risk_score` | ❌ Internal             |
| `admin_notes`         | ❌ Internal             |

---

# 🐍 Task 2 — Build the Python Exporter

## 🎯 Objective

Create a Python application that:

1. Extracts portable fields
2. Generates JSON
3. Generates CSV
4. Excludes internal fields

---

## 📝 Step 1 — Create `exporter.py`

```bash
nano exporter.py
```

Add:

```python
import json
import csv
from sample_data import USER_RECORD

PORTABLE_FIELDS = [
    "user_id",
    "full_name",
    "email",
    "phone",
    "signup_date",
    "preferences"
]


def extract_portable_data(record: dict, fields: list) -> dict:
    """
    Filter the full record down to only portable fields.
    """
    return {
        key: record[key]
        for key in fields
        if key in record
    }


def export_to_json(data: dict, filename: str) -> None:
    """
    Save portable data as JSON.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def export_to_csv(data: dict, filename: str) -> None:
    """
    Save portable data as CSV.
    Nested fields are converted to strings.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(data.keys())

        writer.writerow([
            str(value)
            for value in data.values()
        ])


if __name__ == "__main__":
    portable_data = extract_portable_data(
        USER_RECORD,
        PORTABLE_FIELDS
    )

    export_to_json(
        portable_data,
        "export.json"
    )

    export_to_csv(
        portable_data,
        "export.csv"
    )

    print(
        "Export complete: "
        "export.json and export.csv created."
    )
```

---

## ▶️ Step 2 — Run the Exporter

```bash
python3 exporter.py
```

Expected output:

```text
Export complete: export.json and export.csv created.
```

---

## 📄 Step 3 — Inspect JSON

```bash
cat export.json
```

Example:

```json
{
  "user_id": "U1001",
  "full_name": "Aisha Al Farsi",
  "email": "aisha@example.com",
  "phone": "+971500000000",
  "signup_date": "2023-01-15",
  "preferences": {
    "newsletter": true
  }
}
```

---

## 📊 Step 4 — Inspect CSV

```bash
cat export.csv
```

You should see the portable fields.

### ✨ Technology

![Python](https://img.shields.io/badge/Python-Exporter-3776AB?style=flat-square\&logo=python\&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-Export-000000?style=flat-square\&logo=json\&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-Export-217346?style=flat-square)

---

# 🔐 Task 3 — Sign the Export with GPG

## 🎯 Objective

A detached GPG signature allows us to verify that the exported JSON file has not been modified after signing.

---

## 🔑 Step 1 — Generate a GPG Key

If you don't already have a key:

```bash
gpg --full-generate-key
```

Follow the prompts.

Choose:

* Key type: default
* Key size: default
* Expiration: as required
* Name: your preferred name
* Email: your preferred email
* Passphrase: a secure passphrase

---

## 🔍 Step 2 — List GPG Keys

```bash
gpg --list-keys
```

You should see your newly created key.

### ✨ Technology

![GPG](https://img.shields.io/badge/GPG-Key%20Management-4A4A4A?style=flat-square)

---

## ✍️ Step 3 — Sign the JSON Export

```bash
gpg --output export.json.sig --detach-sign export.json
```

Check the files:

```bash
ls -lh export.json export.json.sig
```

Expected:

```text
export.json
export.json.sig
```

---

## ✅ Step 4 — Verify the Signature

```bash
gpg --verify export.json.sig export.json
```

Expected output contains:

```text
Good signature
```

### 🔐 Security Concept

```text
export.json
     │
     ▼
   GPG
     │
     ▼
export.json.sig
     │
     ▼
Integrity Verification
```

> A digital signature verifies authenticity/integrity; it does **not** encrypt the JSON contents.

### ✨ Technology

![GPG](https://img.shields.io/badge/GPG-Digital%20Signature-4A4A4A?style=flat-square)
![Security](https://img.shields.io/badge/Security-Integrity-6A1B9A?style=flat-square)

---

# 🔄 Task 4 — Transfer the Export Using SFTP

## 🎯 Objective

Use the local OpenSSH SFTP service to simulate secure file delivery.

---

## ⚙️ Step 1 — Check SSH Service

```bash
sudo systemctl status ssh
```

If it is not running:

```bash
sudo systemctl start ssh
```

Enable it at boot if desired:

```bash
sudo systemctl enable ssh
```

---

## 🔗 Step 2 — Connect Using SFTP

```bash
sftp localhost
```

You should receive an SFTP prompt similar to:

```text
sftp>
```

### ✨ Technology

![SFTP](https://img.shields.io/badge/SFTP-Secure%20Transfer-2E8B57?style=flat-square)
![OpenSSH](https://img.shields.io/badge/OpenSSH-Server-000000?style=flat-square\&logo=openssh\&logoColor=white)

---

## 📤 Step 3 — Upload the Export Files

Inside the SFTP prompt:

```text
put export.json
put export.json.sig
put export.csv
```

Then:

```text
exit
```

---

## 🔎 Step 4 — Confirm the Files

```bash
ls -la ~/export.json ~/export.json.sig ~/export.csv
```

You should see all three files.

### 🔄 Secure Transfer Flow

```text
Python Exporter
      │
      ├── export.json
      ├── export.csv
      └── export.json.sig
                │
                ▼
          Local SFTP
                │
                ▼
        Secure File Transfer
```

---

# 📋 Task 5 — Validate JSON with JSON Schema

## 🎯 Objective

Use JSON Schema to confirm that the exported data contains the required fields and expected data types.

---

## 📝 Step 1 — Create `schema.json`

```bash
nano schema.json
```

Add:

```json
{
  "type": "object",
  "required": [
    "user_id",
    "full_name",
    "email",
    "phone",
    "signup_date"
  ],
  "properties": {
    "user_id": {
      "type": "string"
    },
    "full_name": {
      "type": "string"
    },
    "email": {
      "type": "string"
    },
    "phone": {
      "type": "string"
    },
    "signup_date": {
      "type": "string"
    },
    "preferences": {
      "type": "object"
    }
  }
}
```

---

## 🐍 Step 2 — Create `validate.py`

```bash
nano validate.py
```

Add:

```python
import json
from jsonschema import validate, ValidationError


def load_json_file(filename: str) -> dict:
    """Load and return JSON content from a file."""

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def validate_export(
    data_file: str,
    schema_file: str
) -> bool:
    """
    Validate data_file against schema_file.

    Returns:
        True if valid, False otherwise.
    """

    data = load_json_file(data_file)
    schema = load_json_file(schema_file)

    try:
        validate(
            instance=data,
            schema=schema
        )

        print("JSON validation successful.")
        return True

    except ValidationError as error:
        print("JSON validation failed.")
        print(error.message)
        return False


if __name__ == "__main__":
    result = validate_export(
        "export.json",
        "schema.json"
    )

    print(
        "Validation passed!"
        if result
        else "Validation FAILED."
    )
```

---

## ▶️ Step 3 — Run Validation

```bash
python3 validate.py
```

Expected output:

```text
JSON validation successful.
Validation passed!
```

### ✨ Technology

![JSON Schema](https://img.shields.io/badge/JSON%20Schema-Validation-CC2927?style=flat-square)
![Python](https://img.shields.io/badge/Python-Validation-3776AB?style=flat-square\&logo=python\&logoColor=white)

---

# 🧪 Complete Verification

Perform the following checks.

## ✅ Check 1 — Export Files

```bash
ls -la export.json export.csv export.json.sig
```

Expected files:

```text
export.json
export.csv
export.json.sig
```

---

## 🔍 Check 2 — Confirm No Internal Data Leaked

```bash
grep -i "admin_notes\|internal_risk_score" export.json \
&& echo "FAIL: leaked field" \
|| echo "PASS: no internal fields"
```

Expected:

```text
PASS: no internal fields
```

---

## 🔐 Check 3 — Verify GPG Signature

```bash
gpg --verify export.json.sig export.json
```

Expected:

```text
Good signature
```

---

## 📋 Check 4 — Validate JSON

```bash
python3 validate.py
```

Expected:

```text
JSON validation successful.
Validation passed!
```

---

# 🏆 Final Verification Checklist

* [ ] Python exporter completed successfully
* [ ] `export.json` created
* [ ] `export.csv` created
* [ ] Internal fields excluded
* [ ] GPG key created
* [ ] JSON export signed
* [ ] GPG signature verified
* [ ] SSH service running
* [ ] Files transferred through SFTP
* [ ] JSON Schema created
* [ ] JSON export validated successfully

---

# 🛠️ Troubleshooting

## ❌ `gpg: command not found`

Install GPG:

```bash
sudo apt update
sudo apt install -y gnupg
```

Verify:

```bash
gpg --version
```

---

## ❌ SFTP Connection Refused

Check SSH:

```bash
sudo systemctl status ssh
```

Start it:

```bash
sudo systemctl start ssh
```

Try again:

```bash
sftp localhost
```

---

## ❌ `jsonschema` Import Error

Install the package:

```bash
pip3 install jsonschema
```

Verify:

```bash
pip3 show jsonschema
```

---

## ❌ GPG Signature Verification Failed

The file may have changed after it was signed.

Generate a new signature:

```bash
gpg --output export.json.sig --detach-sign export.json
```

Then verify:

```bash
gpg --verify export.json.sig export.json
```

---

## ❌ Empty `export.json`

Check the extraction function:

```python
return {
    key: record[key]
    for key in fields
    if key in record
}
```

Then rerun:

```bash
python3 exporter.py
```

---

# 📂 Project Structure

After completing the lab, your directory should look similar to:

```text
data-portability-lab/
│
├── sample_data.py
├── exporter.py
├── validate.py
├── schema.json
│
├── export.json
├── export.csv
└── export.json.sig
```

---

# 🔐 Security & Privacy Controls Demonstrated

| Control                    | Implementation                         |
| -------------------------- | -------------------------------------- |
| 🛡️ Data Minimization      | Only selected portable fields exported |
| 🔍 Data Classification     | Portable vs internal data identified   |
| 📄 Machine Readability     | JSON and CSV formats                   |
| 🔐 Integrity               | GPG detached signature                 |
| 🔄 Secure Transfer         | SFTP                                   |
| 📋 Data Validation         | JSON Schema                            |
| 🧪 Verification            | Automated checks                       |
| 🚫 Data Leakage Prevention | Internal fields excluded               |

---

# 🧠 Key Learning Outcomes

Through this project, you practiced a complete privacy-oriented data export workflow:

```text
Identify
   ↓
Classify
   ↓
Extract
   ↓
Export
   ↓
Sign
   ↓
Transfer
   ↓
Validate
   ↓
Verify
```

The lab demonstrates how application developers and security engineers can combine **privacy controls, machine-readable formats, cryptographic integrity, secure transfer, and schema validation** into a practical data portability workflow.

---

# 📚 GDPR Article 20 Mapping

This lab provides a simplified technical demonstration of concepts associated with the **GDPR right to data portability**.

| GDPR Concept            | Lab Implementation       |
| ----------------------- | ------------------------ |
| Data portability        | Portable data extraction |
| Structured format       | JSON / CSV               |
| Machine-readable format | JSON                     |
| User-provided data      | Selected portable fields |
| Secure handling         | GPG + SFTP               |
| Data integrity          | Detached GPG signature   |
| Validation              | JSON Schema              |

> ⚠️ This project is a technical learning exercise and should not be treated as a complete legal interpretation of GDPR Article 20.

---

# 🚀 Skills Demonstrated

```text
🐍 Python Development
📄 JSON Processing
📊 CSV Processing
🔐 GPG Digital Signatures
🔄 SFTP File Transfer
📋 JSON Schema Validation
🐧 Linux Administration
🛡️ Data Privacy
🔍 Data Classification
🔒 Data Integrity
🧪 Security Verification
```

---

# 🌟 Conclusion

This hands-on lab implemented a simplified **GDPR Article 20 data portability workflow** from beginning to end.

You learned how to identify portable user data, build a Python-based exporter, generate JSON and CSV files, protect the JSON export using a GPG digital signature, transfer files securely through SFTP, and validate the exported data against a JSON Schema.

The project provides practical experience at the intersection of:

**Privacy Engineering + Python + Linux + Cryptography + Secure File Transfer + Data Validation**

---

<p align="center">

### 🔐 Privacy by Design • Secure by Default • Machine Readable

**Data Portability Lab**

</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Security-GPG%20Signed-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Validation-JSON%20Schema-orange?style=for-the-badge">
</p>
