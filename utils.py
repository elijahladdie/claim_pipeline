import logging
import os

def setup_logging():
    """Configure logging with file + console handlers."""
    os.makedirs("results", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("results/pipeline.log"),
            logging.StreamHandler()
        ]
    )
