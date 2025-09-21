import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from etl.loaders import load
from etl.transformations import parse_to_dataframes

logging.basicConfig(level=logging.INFO)
BASE_DIR = Path(__file__).resolve().parents[1]


def extract_data() -> list[dict[str, Any]]:
    data_path = BASE_DIR / "data" / "orders_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        raw_json = json.load(f)
    return raw_json


def main() -> None:
    logging.info("Starting ETL pipeline...")
    raw_json: list[dict[str, Any]] = extract_data()
    dfs: dict[str, pd.DataFrame] = parse_to_dataframes(raw_json)
    load(dfs)
    logging.info("ETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
