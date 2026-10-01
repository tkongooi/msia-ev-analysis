"""Download, cache and clean Malaysian car registration data (data.gov.my)."""
from pathlib import Path

import pandas as pd

BASE_URL = "https://storage.data.gov.my/transportation/cars_{year}.parquet"
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def fetch_year(year: int, refresh: bool = False) -> pd.DataFrame:
    """Return one year of registrations, cached under data/ after first download."""
    path = DATA_DIR / f"cars_{year}.parquet"
    if refresh or not path.exists():
        DATA_DIR.mkdir(exist_ok=True)
        pd.read_parquet(BASE_URL.format(year=year)).to_parquet(path)
    return pd.read_parquet(path)


def load(years=(2024, 2025, 2026), refresh: bool = False) -> pd.DataFrame:
    """Load and clean all years into one frame. One row = one registered car.

    Adds `year`, `month` (1-12) and `period` (monthly Period) columns.
    """
    df = pd.concat([fetch_year(y, refresh) for y in years], ignore_index=True)
    df["date_reg"] = pd.to_datetime(df["date_reg"])
    for col in ("maker", "model"):
        df[col] = df[col].str.strip()
    df["year"] = df["date_reg"].dt.year
    df["month"] = df["date_reg"].dt.month
    df["period"] = df["date_reg"].dt.to_period("M")
    return df
