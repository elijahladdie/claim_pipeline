from datetime import datetime

# Fixed "today" (2025-07-30 as per case study)
TODAY = datetime(2025, 7, 30)

# Output files
OUTPUT_FILE = "results/resubmission_candidates.json"
REJECTION_LOG = "results/rejected_records.json"

# Business rules
RETRYABLE_REASONS = {"Missing modifier", "Incorrect NPI", "Prior auth required"}
NON_RETRYABLE_REASONS = {"Authorization expired", "Incorrect provider type"}
