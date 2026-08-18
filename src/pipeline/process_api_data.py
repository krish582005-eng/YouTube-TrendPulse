import pandas as pd
from pathlib import Path


# ------------------------------------------------
# Project root
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


# ------------------------------------------------
# Input
# ------------------------------------------------

input_file = (
    BASE_DIR
    / "data"
    / "raw"
    / "youtube_api_data.csv"
)


# ------------------------------------------------
# Load
# ------------------------------------------------

df = pd.read_csv(
    input_file
)


# ------------------------------------------------
# Basic cleaning
# ------------------------------------------------

df["views"] = pd.to_numeric(
    df["views"],
    errors="coerce"
)

df["likes"] = pd.to_numeric(
    df["likes"],
    errors="coerce"
)

df["comments"] = pd.to_numeric(
    df["comments"],
    errors="coerce"
)


df = df.drop_duplicates(
    subset="video_id"
)


# ------------------------------------------------
# Report
# ------------------------------------------------

print("\nAPI data validation completed.")

print(
    "Videos:",
    len(df)
)

print(
    "Columns:",
    list(df.columns)
)

print("\nMissing values:")

print(
    df.isnull().sum()
)

print("\nTop videos by views:")

print(
    df[
        [
            "video_id",
            "title",
            "views"
        ]
    ]
    .sort_values(
        "views",
        ascending=False
    )
    .head(10)
)