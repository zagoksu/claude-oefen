"""Read a CSV, clean it, and write the result out as Parquet."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, drop empty rows, and remove exact duplicates."""
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    df = df.dropna(how="all")
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def transform_csv_to_parquet(input_path: Path, output_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    cleaned = clean(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(output_path, index=False)
    return cleaned


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="Path to the source CSV file")
    parser.add_argument("output_parquet", type=Path, help="Path to write the cleaned Parquet file")
    args = parser.parse_args()

    transform_csv_to_parquet(args.input_csv, args.output_parquet)


if __name__ == "__main__":
    main()
