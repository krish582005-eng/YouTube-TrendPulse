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

database_file = (
    BASE_DIR
    / "youtube_trendpulse.db"
)

output_file = (
    BASE_DIR
    / "data"
    / "processed"
    / "api_velocity.csv"
)


# ------------------------------------------------
# Load SQLite history
# ------------------------------------------------

connection = sqlite3.connect(
    database_file
)

try:

    df = pd.read_sql_query(
        "SELECT * FROM youtube_history",
        connection
    )

finally:

    connection.close()


if df.empty:
    raise ValueError(
        "youtube_history is empty."
    )


print("\nHistorical data loaded.")
print(
    "Historical rows:",
    len(df)
)


# ------------------------------------------------
# Convert data
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

df["collected_at"] = pd.to_datetime(
    df["collected_at"],
    errors="coerce"
)


# ------------------------------------------------
# Remove invalid records
# ------------------------------------------------

df = df.dropna(
    subset=[
        "video_id",
        "views",
        "collected_at"
    ]
)


# ------------------------------------------------
# Sort history
# ------------------------------------------------

df = df.sort_values(
    [
        "video_id",
        "collected_at"
    ]
).reset_index(drop=True)


# ------------------------------------------------
# Previous views
# ------------------------------------------------

df["previous_views"] = (
    df.groupby("video_id")["views"]
    .shift(1)
)


# ------------------------------------------------
# Previous timestamp
# ------------------------------------------------

df["previous_time"] = (
    df.groupby("video_id")["collected_at"]
    .shift(1)
)


# ------------------------------------------------
# Time difference
# ------------------------------------------------

df["time_diff_hours"] = (
    (
        df["collected_at"]
        - df["previous_time"]
    )
    .dt.total_seconds()
    / 3600
)


# ------------------------------------------------
# View change
# ------------------------------------------------

df["view_change"] = (
    df["views"]
    - df["previous_views"]
)


# ------------------------------------------------
# Growth percentage
# ------------------------------------------------

df["view_growth_pct"] = (
    df["view_change"]
    /
    df["previous_views"].replace(
        0,
        pd.NA
    )
)


# ------------------------------------------------
# View velocity
# ------------------------------------------------

df["view_velocity"] = (
    df["view_change"]
    /
    df["time_diff_hours"].replace(
        0,
        pd.NA
    )
)


# ------------------------------------------------
# Save
# ------------------------------------------------

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------
# Result
# ------------------------------------------------

print("\nVelocity calculation completed.")

print(
    "Rows processed:",
    len(df)
)

print(
    "Unique videos:",
    df["video_id"].nunique()
)

print(
    "Output:",
    output_file
)