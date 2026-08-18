import sqlite3
import pandas as pd
from pathlib import Path


# ------------------------------------------------
# Project root
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


# ------------------------------------------------
# Files
# ------------------------------------------------

input_file = (
    BASE_DIR
    / "data"
    / "raw"
    / "youtube_api_data.csv"
)

database_file = (
    BASE_DIR
    / "youtube_trendpulse.db"
)


# ------------------------------------------------
# Load latest API data
# ------------------------------------------------

df = pd.read_csv(input_file)


if df.empty:
    raise ValueError(
        "youtube_api_data.csv is empty."
    )


# ------------------------------------------------
# Add collection timestamp
# ------------------------------------------------

collection_time = pd.Timestamp.now()

df["collected_at"] = collection_time


# ------------------------------------------------
# SQLite
# ------------------------------------------------

connection = sqlite3.connect(
    database_file
)

try:

    # IMPORTANT:
    # APPEND = preserve ALL history

    df.to_sql(
        "youtube_history",
        connection,
        if_exists="append",
        index=False
    )

    connection.commit()

finally:

    connection.close()


# ------------------------------------------------
# Result
# ------------------------------------------------

print("\nHistorical snapshot stored.")

print(
    "Rows added:",
    len(df)
)

print(
    "Collection time:",
    collection_time
)

print(
    "Database:",
    database_file
)