# **Healthcare Claim Resubmission Pipeline**

## **Overview**

This pipeline processes healthcare claims from multiple EMR sources, normalizes them, checks eligibility, and outputs:

* **Eligible claims** ready for resubmission (`resubmission_candidates.json`)
* **Rejected claims** with **rejection reasons** (`rejected_records.json`)

It also logs all processing steps for traceability.

---

## **Features**

* Loads claims from CSV and JSON sources.
* Normalizes different schemas to a common format.
* Applies eligibility rules based on claim status, required fields, and retryable denial reasons.
* Generates clear, rule-based rejection reasons for failed claims.
* Outputs results as JSON files and logs processing details.

---

## **Directory Structure**

```
project/
│
├─ data/
│   ├─ emr_alpha.csv
│   └─ emr_beta.json
├─ config.py
├─ ingestion.py
├─ normalization.py
├─ eligibility.py
├─ output.py
├─ utils.py
├─ main.py
└─ README.md
```

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/elijahladdie/claim_pipeline
cd claim_pipeline
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## **Usage**

Run the pipeline:

```bash
python main.py
```

* `resubmission_candidates.json`  eligible claims for resubmission.
* `rejected_records.json`  rejected claims with rule-based rejection reasons.

---

## **Testing Example**

**Sample input:**

`data/emr_alpha.csv`

```csv
claim_id,patient_id,claim_amount,status,denial_reason,submitted_at
101,1001,500,denied,Missing modifier,2025-07-01
102,,300,denied,,2025-07-05
```

`data/emr_beta.json`

```json
[
  {"claim_id": "201", "patient_id": "2001", "claim_amount": 1000, "status": "denied", "denial_reason": "Authorization expired", "submitted_at": "2025-07-03"}
]
```

**Sample output (`rejected_records.json`):**

```json
[
  {
    "claim_id": "102",
    "patient_id": null,
    "claim_amount": 300,
    "rejection_reason": "Missing patient ID; cannot process claim."
  },
  {
    "claim_id": "201",
    "patient_id": "2001",
    "claim_amount": 1000,
    "rejection_reason": "Denial reason 'Authorization expired' is non-retryable; cannot resubmit."
  }
]
```

---

## **Logging**

* Console logs include claims processed, number of eligible and rejected claims, and reasons for rejection.