# Weather Insights AI

An agentic data engineering pipeline built with Python and Google Agent Development Kit (ADK).

## Project Overview

Weather Insights AI retrieves historical weather data for Bloomington, Indiana, processes the data using pandas, stores the results in Google Cloud Storage, and displays the analysis through a Flask dashboard.

A Gemini-powered ADK agent initiates the pipeline through a custom Python function tool.

## Technologies

- Python 3.12
- Google Agent Development Kit (ADK)
- Gemini
- Open-Meteo Historical Weather API
- pandas
- Google Cloud Storage
- Flask
- Chart.js

## Pipeline Steps

1. **Data ingestion:** Retrieve daily maximum temperature and precipitation from the Open-Meteo API.
2. **Data processing:** Remove missing values, filter observations to October 1–7, 2025, classify rainy and dry days, group records, and calculate aggregates.
3. **Cloud storage:** Upload the processed JSON data to Google Cloud Storage.
4. **Agent orchestration:** Use Gemini and Google ADK to trigger the complete pipeline.
5. **Visualization:** Use Flask and Chart.js to display the stored statistics and daily weather trends.

## Setup

### 1. Clone the repository

```bash
git clone [YOUR_GITHUB_REPOSITORY_URL](https://github.com/atmikha/weather-insights-ai.git)
cd weather-insights-ai
```

### 2. Create a Python environment

Install Python 3.12 and create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure API credentials

Create a `.env` file containing:

```text
GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_API_KEY
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GCS_BUCKET_NAME=YOUR_BUCKET_NAME
```

Create or select a Google Cloud project with an accessible Cloud Storage bucket.

Install the Google Cloud CLI and authenticate:

```bash
gcloud auth application-default login
```

Your Google account must have permission to read and write objects in the selected bucket.

### 4. Run the complete pipeline through the ADK agent

```bash
python run_agent.py
```

The agent will call the pipeline tool, process the weather observations, and upload the results to Google Cloud Storage.

### 5. Run the pipeline directly (optional)

```bash
python storage.py
```

### 6. Launch the dashboard

```bash
python app.py
```

Open:

http://127.0.0.1:5000

The dashboard reads the stored JSON file from Google Cloud Storage and displays weather statistics and charts.

## Example Results

Historical period: October 1–7, 2025

- Average daily maximum temperature: 27.3°C
- Total precipitation: 38.4 mm
- Days analyzed: 7

## Data Source

Open-Meteo Historical Weather API:

https://open-meteo.com/en/docs/historical-weather-api

## Security

The Cloud Storage bucket is private. Local Application Default Credentials authenticate the Python program. API keys and credential files are excluded from Git through `.gitignore`.

## Future Improvements

See `FUTURE_IMPROVEMENTS.md` for proposed improvements to the pipeline.
