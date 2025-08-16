import logging
from datetime import timedelta
from config import TODAY, RETRYABLE_REASONS, NON_RETRYABLE_REASONS

def is_retryable(reason: str) -> bool:
    """Return True if denial reason is retryable (or ambiguous treated as retryable)."""
    if not reason:
        # Missing reason  treat as ambiguous (non-retryable by default)
        logging.warning("Denial reason is missing  treated as non-retryable.")
        return False
    reason_lower = reason.lower()
    if reason_lower in map(str.lower, RETRYABLE_REASONS):
        return True
    if reason_lower in map(str.lower, NON_RETRYABLE_REASONS):
        return False
    # Ambiguous reason  treat as retryable
    logging.warning(f"Ambiguous denial reason '{reason}'  treated as retryable.")
    return True


def check_eligibility(record: dict) -> tuple[dict | None, str | None]:
    """
    Apply business rules and return:
        - eligible_record if eligible
        - rejection_reason if rejected
    """
    try:
        # Not denied
        if record.get("status", "").lower() != "denied":
            return None, "Claim is not denied; no resubmission required."

        # Missing patient ID
        if not record.get("patient_id"):
            return None, "Missing patient ID; cannot process claim."

        # Missing procedure code
        if not record.get("procedure_code"):
            return None, "Missing procedure code; cannot process claim."

        # Submitted too recently
        submitted_at = record.get("submitted_at")
        if not submitted_at or (TODAY.date() - submitted_at) <= timedelta(days=7):
            return None, "Claim submitted within 7 days; resubmission not allowed yet."

        # Retryable denial reason check
        denial_reason = record.get("denial_reason")
        if not is_retryable(denial_reason):
            return None, f"Denial reason '{denial_reason}' is non-retryable; cannot resubmit."

        # Eligible claim
        eligible_record = {
            "claim_id": record["claim_id"],
            "resubmission_reason": denial_reason or "Ambiguous reason",
            "source_system": record["source_system"],
            "recommended_changes": f"Review {denial_reason or 'claim details'} and resubmit"
        }
        return eligible_record, None

    except Exception as e:
        logging.error(f"Eligibility check failed for claim {record.get('claim_id')}: {e}")
        return None, f"Eligibility check error: {e}"
