import pandas as pd
from pathlib import Path


# ============================================================
# YOUTUBE TRENDPULSE — TREND SCORE ENGINE
# ============================================================

print("\n" + "=" * 60)
print("TREND SCORE ENGINE")
print("=" * 60)


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

input_file = (
    BASE_DIR
    / "data"
    / "processed"
    / "api_velocity.csv"
)

output_file = (
    BASE_DIR
    / "data"
    / "processed"
    / "api_trend_scores.csv"
)


# ------------------------------------------------------------
# 2. LOAD VELOCITY DATA
# ------------------------------------------------------------

df = pd.read_csv(input_file)

print(f"Historical rows loaded: {len(df)}")


# ------------------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# ------------------------------------------------------------

required_columns = [
    "video_id",
    "title",
    "channel_title",
    "views",
    "likes",
    "comments",
    "collected_at",
    "view_growth_pct",
    "view_velocity"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:
        print("-", column)

    raise ValueError(
        "Required columns are missing from api_velocity.csv"
    )


# ------------------------------------------------------------
# 4. CONVERT DATA TYPES
# ------------------------------------------------------------

df["collected_at"] = pd.to_datetime(
    df["collected_at"],
    errors="coerce"
)

numeric_columns = [
    "views",
    "likes",
    "comments",
    "view_growth_pct",
    "view_velocity"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ------------------------------------------------------------
# 5. REMOVE INVALID VIDEO IDs
# ------------------------------------------------------------

df = df.dropna(
    subset=["video_id"]
)

df["video_id"] = (
    df["video_id"]
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# 6. KEEP LATEST SNAPSHOT FOR EACH VIDEO
# ------------------------------------------------------------

df = (
    df.sort_values("collected_at")
      .drop_duplicates(
          subset="video_id",
          keep="last"
      )
      .copy()
)

print(
    f"Unique videos monitored: {df['video_id'].nunique()}"
)


# ------------------------------------------------------------
# 7. ENGAGEMENT RATE
# ------------------------------------------------------------

df["engagement_rate"] = (
    (df["likes"] + df["comments"])
    /
    df["views"].replace(0, pd.NA)
)


# ------------------------------------------------------------
# 8. HANDLE MISSING VALUES
# ------------------------------------------------------------

df["view_growth_pct"] = (
    df["view_growth_pct"]
    .fillna(0)
)

df["view_velocity"] = (
    df["view_velocity"]
    .fillna(0)
)

df["engagement_rate"] = (
    df["engagement_rate"]
    .fillna(0)
)


# ------------------------------------------------
# 9. POSITIVE METRICS
# ------------------------------------------------

# Negative growth should not increase the trend score
df["positive_growth"] = df["view_growth_pct"].clip(lower=0)

df["positive_velocity"] = df["view_velocity"].clip(lower=0)


# ------------------------------------------------
# 10. PERCENTILE SCORE
# ------------------------------------------------

def percentile_score(series):

    if series.nunique() <= 1:
        return pd.Series(
            50,
            index=series.index
        )

    return (
        series.rank(
            method="average",
            pct=True
        ) * 100
    )


# ------------------------------------------------
# 11. COMPONENT SCORES
# ------------------------------------------------

df["growth_score"] = percentile_score(
    df["positive_growth"]
)

df["velocity_score"] = percentile_score(
    df["positive_velocity"]
)

df["engagement_score"] = percentile_score(
    df["engagement_rate"]
)


# ------------------------------------------------
# 12. TREND SCORE
# ------------------------------------------------

df["emerging_trend_score"] = (

    df["growth_score"] * 0.35

    +

    df["velocity_score"] * 0.45

    +

    df["engagement_score"] * 0.20

).round(2)


# ------------------------------------------------
# 13. TREND CLASSIFICATION
# ------------------------------------------------

def classify_trend(score):

    if score >= 70:
        return "Emerging"

    elif score >= 50:
        return "Growing"

    elif score >= 30:
        return "Stable"

    else:
        return "Normal"


df["emerging_status"] = (
    df["emerging_trend_score"]
    .apply(classify_trend)
)


# ------------------------------------------------
# 14. TREND ALERT
# ------------------------------------------------

df["trend_alert"] = df[
    "emerging_trend_score"
].apply(
    lambda score:
        "TREND ALERT"
        if score >= 70
        else "NO ALERT"
)

# ------------------------------------------------------------
# 14. CREATE TREND ALERT
# ------------------------------------------------------------

df["trend_alert"] = df[
    "emerging_trend_score"
].apply(

    lambda score:
        "TREND ALERT"
        if score >= 70
        else "NO ALERT"

)


# ------------------------------------------------------------
# 15. SORT BY TREND SCORE
# ------------------------------------------------------------

df = (
    df.sort_values(
        "emerging_trend_score",
        ascending=False
    )
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 16. SAVE FINAL TREND DATA
# ------------------------------------------------------------

df.to_csv(
    output_file,
    index=False
)


# ------------------------------------------------------------
# 17. DISPLAY RESULTS
# ------------------------------------------------------------

print("\nTrend score calculation completed.")

print(
    f"Unique videos: {df['video_id'].nunique()}"
)

print(
    f"Maximum trend score: "
    f"{df['emerging_trend_score'].max():.2f}"
)

print(
    f"Average trend score: "
    f"{df['emerging_trend_score'].mean():.2f}"
)


print("\n" + "=" * 42)
print("TREND STATUS")
print("=" * 42)

print(
    df["emerging_status"]
    .value_counts()
)


print("\n" + "=" * 42)
print("TOP 10 TREND VIDEOS")
print("=" * 42)

print(

    df[
        [
            "video_id",
            "title",
            "views",
            "view_growth_pct",
            "view_velocity",
            "engagement_rate",
            "emerging_trend_score",
            "emerging_status",
            "trend_alert"
        ]
    ]
    .head(10)
    .to_string(index=False)

)


print("\nOutput:")
print(output_file)

print("\n" + "=" * 60)