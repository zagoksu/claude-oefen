from pathlib import Path

import pandas as pd

from src.transform import clean, transform_csv_to_parquet


def test_clean_normalizes_column_names():
    df = pd.DataFrame({"First Name": ["a"], " Last Name ": ["b"]})
    result = clean(df)
    assert list(result.columns) == ["first_name", "last_name"]


def test_clean_drops_duplicates_and_empty_rows():
    df = pd.DataFrame(
        {
            "a": [1, 1, None, 2],
            "b": [1, 1, None, 2],
        }
    )
    result = clean(df)
    assert len(result) == 2
    assert result["a"].tolist() == [1, 2]


def test_transform_csv_to_parquet_roundtrip(tmp_path: Path):
    csv_path = tmp_path / "input.csv"
    parquet_path = tmp_path / "out" / "output.parquet"

    csv_path.write_text("Name,Age\nAlice,30\nAlice,30\nBob,25\n")

    cleaned = transform_csv_to_parquet(csv_path, parquet_path)

    assert parquet_path.exists()
    assert list(cleaned.columns) == ["name", "age"]
    assert len(cleaned) == 2

    read_back = pd.read_parquet(parquet_path)
    pd.testing.assert_frame_equal(read_back, cleaned)
