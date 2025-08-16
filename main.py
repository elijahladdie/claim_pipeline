import pandas as pd
import logging

from utils import setup_logging
from ingestion import load_csv, load_json
from normalization import normalize_schema
from eligibility import check_eligibility
from output import save_json
from config import OUTPUT_FILE, REJECTION_LOG

def run_pipeline():
    setup_logging()
    logging.info("Pipeline started.")

    # Load sources
    df_alpha = load_csv("data/emr_alpha.csv", "alpha")
    df_beta = load_json("data/emr_beta.json", "beta")

    # Normalize
    df_alpha = normalize_schema(df_alpha, "alpha")
    df_beta = normalize_schema(df_beta, "beta")
    all_claims = pd.concat([df_alpha, df_beta], ignore_index=True)

    logging.info(f"Claims loaded: {len(all_claims)} (alpha={len(df_alpha)}, beta={len(df_beta)})")

    candidates, rejected = [], []

    # Apply eligibility logic
    for _, row in all_claims.iterrows():
        record = row.to_dict()
        eligible_record, rejection_reason = check_eligibility(record)

        if eligible_record:
            candidates.append(eligible_record)
        else:
            # Add explicit rejection reason to the record
            record["rejection_reason"] = rejection_reason or "Unknown reason"
            rejected.append(record)
            logging.info(f"Claim rejected: {rejection_reason} | Claim ID: {record.get('claim_id')}")

    # Save results
    save_json(candidates, OUTPUT_FILE)
    save_json(rejected, REJECTION_LOG)

    logging.info(f"Eligible: {len(candidates)} | Rejected: {len(rejected)}")
    logging.info("Pipeline finished.")

if __name__ == "__main__":
    run_pipeline()
