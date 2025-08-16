import pandas as pd
import logging

def load_csv(path: str, source: str) -> pd.DataFrame:
    """Load claims from CSV file."""
    try:
        df = pd.read_csv(path)
        df["source_system"] = source
        return df
    except Exception as e:
        logging.error(f"CSV ingestion failed ({path}): {e}")
        return pd.DataFrame()


def load_json(path: str, source: str) -> pd.DataFrame:
    """Load claims from JSON file."""
    try:
        df = pd.read_json(path)
        df["source_system"] = source
        return df
    except Exception as e:
        logging.error(f"JSON ingestion failed ({path}): {e}")
        return pd.DataFrame()
