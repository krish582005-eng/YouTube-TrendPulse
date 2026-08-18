import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


# Load .env
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_youtube_client():

    if not API_KEY:
        raise ValueError(
            "YOUTUBE_API_KEY not found. "
            "Check your .env file."
        )

    return build(
        "youtube",
        "v3",
        developerKey=API_KEY
    )