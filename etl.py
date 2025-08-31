# etl.py
from pathlib import Path
import pandas as pd

RAW = Path("data_raw.csv")
OUT = Path("data.csv")


def make_sample_data(path: Path = RAW):
    # Tiny example dataset
    df = pd.DataFrame(
        {
            "year": [2020, 2021, 2020, 2021, 2022, 2022],
            "city": ["London", "London", "Manchester", "Manchester", "Leeds", "Leeds"],
            "price": [500000, 520000, 250000, 270000, 210000, 230000],
        }
    )
    df.to_csv(path, index=False)


def load_and_clean(in_path: Path, out_path: Path):
    df = pd.read_csv(in_path)
    # Simple cleaning examples
    df = df.dropna()
    df["year"] = df["year"].astype(int)
    df["city"] = df["city"].str.strip()
    df["price"] = df["price"].astype(float)

    df.to_csv(out_path, index=False)
    return df


if __name__ == "__main__":
    if not RAW.exists():
        make_sample_data(RAW)
    df = load_and_clean(RAW, OUT)
    print("Saved cleaned data to", OUT.resolve())
    print(df.head())
