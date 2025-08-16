import pandas as pd

def normalize_schema(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """
    Convert incoming records into the unified schema:
    claim_id, patient_id, procedure_code, denial_reason,
    status, submitted_at, source_system
    """
    mappings = {
        "alpha": {
            "claim_id": "claim_id",
            "patient_id": "patient_id",
            "procedure_code": "procedure_code",
            "denial_reason": "denial_reason",
            "status": "status",
            "submitted_at": "submitted_at",
        },
        "beta": {
            "id": "claim_id",
            "member": "patient_id",
            "code": "procedure_code",
            "error_msg": "denial_reason",
            "status": "status",
            "date": "submitted_at",
        }
    }

    schema = [
        "claim_id", "patient_id", "procedure_code",
        "denial_reason", "status", "submitted_at", "source_system"
    ]

    # Rename columns to match unified schema
    df = df.rename(columns=mappings[source])

    # Ensure required fields exist
    for col in schema:
        if col not in df.columns:
            df[col] = None

    # Normalize dates  ensure ISO format
    df["submitted_at"] = pd.to_datetime(df["submitted_at"], errors="coerce").dt.date

    return df[schema]
