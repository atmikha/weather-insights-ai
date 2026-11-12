
import json
import os

from dotenv import load_dotenv
from google.cloud import storage

from process_data import process_weather_data


load_dotenv()

PROJECT_ID = os.getenv(
    "GOOGLE_CLOUD_PROJECT", "weather-insights-ai"
)

BUCKET_NAME = os.getenv(
    "GCS_BUCKET_NAME", "weather-insights-ai-2026-aj"
)

FILE_NAME = "weather_summary.json"


def upload_weather_data(data: dict) -> dict:
    """Upload processed weather results to Google Cloud Storage."""

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_NAME)

    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type="application/json",
    )

    return {
        "status": "success",
        "bucket": BUCKET_NAME,
        "file_name": FILE_NAME,
        "message": "Weather data uploaded successfully",
    }


def get_stored_weather_data() -> dict:
    """Download the latest weather results from Cloud Storage."""

    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_NAME)

    json_text = blob.download_as_text()

    return json.loads(json_text)


def run_weather_pipeline() -> dict:
    """Fetch, process, and upload Bloomington weather data.

    Returns:
        A dictionary containing the pipeline status and summary.
    """

    print("1. Fetching and processing weather data...", flush=True)
    weather = process_weather_data()

    print("2. Uploading results to Google Cloud Storage...", flush=True)
    upload_result = upload_weather_data(weather)

    print("3. Pipeline completed successfully.", flush=True)

    return {
        "status": "success",
        "location": weather["location"],
        "start_date": weather["start_date"],
        "end_date": weather["end_date"],
        "average_max_temperature": weather["average_max_temperature"],
        "total_precipitation": weather["total_precipitation"],
        "number_of_days": weather["number_of_days"],
        "storage_bucket": upload_result["bucket"],
        "storage_file": upload_result["file_name"],
    }


if __name__ == "__main__":
    result = run_weather_pipeline()
    print(json.dumps(result, indent=2))
