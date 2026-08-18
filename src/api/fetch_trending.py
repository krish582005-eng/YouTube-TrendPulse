from youtube_client import get_youtube_client
from pathlib import Path
import csv


# ------------------------------------------------
# YouTube client
# ------------------------------------------------

youtube = get_youtube_client()


# ------------------------------------------------
# Fetch trending videos in India
# ------------------------------------------------

request = youtube.videos().list(
    part="snippet,statistics",
    chart="mostPopular",
    regionCode="IN",
    maxResults=50
)

response = request.execute()


# ------------------------------------------------
# Project root
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


# ------------------------------------------------
# Output
# ------------------------------------------------

output_file = (
    BASE_DIR
    / "data"
    / "raw"
    / "youtube_api_data.csv"
)


# ------------------------------------------------
# Extract data
# ------------------------------------------------

rows = []

for video in response.get("items", []):

    snippet = video.get("snippet", {})
    statistics = video.get("statistics", {})

    rows.append({
        "video_id": video["id"],
        "title": snippet.get("title", ""),
        "channel_title": snippet.get(
            "channelTitle",
            ""
        ),
        "published_at": snippet.get(
            "publishedAt",
            ""
        ),
        "category_id": snippet.get(
            "categoryId",
            ""
        ),
        "views": statistics.get(
            "viewCount",
            0
        ),
        "likes": statistics.get(
            "likeCount",
            0
        ),
        "comments": statistics.get(
            "commentCount",
            0
        )
    })


# ------------------------------------------------
# Save latest API snapshot
# ------------------------------------------------

fieldnames = [
    "video_id",
    "title",
    "channel_title",
    "published_at",
    "category_id",
    "views",
    "likes",
    "comments"
]


with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)


# ------------------------------------------------
# Result
# ------------------------------------------------

print("\nYouTube API fetch completed.")
print("Videos fetched:", len(rows))
print("File saved to:", output_file)