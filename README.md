# Weather Insights AI

An end-to-end agentic data engineering pipeline built with Python and Google's Agent Development Kit (ADK).

## Project Overview

Weather Insights AI retrieves historical weather data from a public API, processes it using pandas, stores the results in Google Cloud Storage, and visualizes the processed data through a Flask web dashboard.

The project analyzes daily maximum temperatures and precipitation in Bloomington, Indiana, from **October 1–7, 2025**.

A Gemini-powered Google ADK agent initiates the data engineering workflow through a custom Python tool.

## Technologies Used

- **Python 3.12** — Core programming language
- **Google Agent Development Kit (ADK)** — AI agent orchestration
- **Gemini** — Language model used by the agent
- **Open-Meteo Historical Weather API** — Public weather data source
- **pandas** — Data cleaning, filtering, grouping, and aggregation
- **Google Cloud Storage** — Cloud object storage
- **Flask** — Python web application
- **Chart.js** — HTML dashboard visualizations

## Pipeline Architecture

The application follows this workflow:

```text
User runs the ADK agent
          |
          v
Google ADK Agent (Gemini)
          |
          v
run_weather_pipeline() tool
          |
          v
Open-Meteo API (Data Ingestion)
          |
          v
pandas (Data Processing)
          |
          v
Google Cloud Storage (JSON)
          |
          v
Flask Web Application
          |
          v
HTML Dashboard (Chart.js)
```

### 1. Data Ingestion

The pipeline retrieves historical weather data for Bloomington, Indiana, using the public Open-Meteo API.

The retrieved fields include:

- Date
- Daily maximum temperature (°C)
- Daily precipitation (mm)

The data is retrieved by `api.py`.

### 2. Data Processing

The `process_data.py` script uses pandas to transform the API response.

Processing includes:

- Converting API results into a pandas DataFrame
- Removing records with missing values
- Converting and sorting dates
- Filtering data to October 1–7, 2025
- Classifying days as rainy or dry
- Grouping records by weather type
- Aggregating temperature and precipitation statistics

The pipeline calculates the average daily maximum temperature, total precipitation, number of days analyzed, and statistics for rainy versus dry days.

It also retains daily observations for visualization.

### 3. Cloud Storage

The `storage.py` module uploads the processed results to Google Cloud Storage.

The output is stored as:

`weather_summary.json`

The JSON contains the calculated statistics, grouped weather results, and daily observations.

The bucket is private and accessed through authenticated Google Cloud client libraries.

### 4. Agentic Orchestration

The project uses Google's Agent Development Kit (ADK) to build a Gemini-powered agent.

The agent is defined in `agent.py` and executed through `run_agent.py`.

The agent has access to a custom function tool:

`run_weather_pipeline()`

When instructed to run the weather pipeline, the agent invokes this tool. The tool coordinates the following operations:

1. Retrieve historical weather data from Open-Meteo.
2. Clean, filter, group, and aggregate the data using pandas.
3. Upload the processed results to Google Cloud Storage.
4. Return the pipeline status and calculated statistics to the agent.

The agent then summarizes the execution results, including the cloud storage destination.

This allows the workflow to be initiated and monitored through an ADK agent rather than requiring the user to manually execute each processing step.

### 5. Visualization

The Flask application in `app.py` retrieves the stored JSON data from Google Cloud Storage.

The HTML dashboard in `templates/index.html` displays:

- Average daily maximum temperature
- Total precipitation
- Number of days analyzed
- Daily maximum temperature line chart
- Daily precipitation bar chart
- Grouped weather summary comparing rainy and dry days

Chart.js provides the visualizations.

The dashboard runs locally at:

http://127.0.0.1:5000

## Project Structure

```text
weather-insights-ai/
│
├── agent.py
├── api.py
├── app.py
├── check_models.py
├── process_data.py
├── run_agent.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── templates/
    └── index.html
```

## Setup and Installation

### Prerequisites

To run this project, you need:

- Python 3.12
- Git
- A Google AI Studio API key with access to the configured Gemini model
- A Google Cloud project
- A Google Cloud Storage bucket
- Google Cloud CLI for local authentication

### Step 1: Clone the repository

Open a terminal and run:

```bash
git clone https://github.com/atmikha/weather-insights-ai.git
cd weather-insights-ai
```

### Step 2: Create a Python virtual environment

Create a virtual environment using Python 3.12:

```bash
python3.12 -m venv .venv
```

Activate the environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### Step 3: Configure Google Cloud Storage

Create or select a Google Cloud project.

In Google Cloud Console:

1. Open Cloud Storage.
2. Create a bucket with a globally unique name.
3. Select a region and Standard storage class.
4. Keep public access prevention enabled.
5. Use Uniform bucket-level access.

The account running the application must have permission to read and write objects in the bucket.

### Step 4: Configure environment variables

Create a file named `.env` in the project's root directory.

Add:

```env
GOOGLE_API_KEY=YOUR_GOOGLE_AI_STUDIO_API_KEY
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=YOUR_GOOGLE_CLOUD_PROJECT_ID
GCS_BUCKET_NAME=YOUR_GOOGLE_CLOUD_STORAGE_BUCKET_NAME
```

Replace the placeholder values with your own credentials and cloud resource identifiers.

Do not commit `.env` to GitHub.

### Step 5: Authenticate with Google Cloud

Install Google Cloud CLI using the official instructions:

https://cloud.google.com/sdk/docs/install

Sign in:

```bash
gcloud auth login
```

Set the project:

```bash
gcloud config set project YOUR_GOOGLE_CLOUD_PROJECT_ID
```

Configure Application Default Credentials for the Python client library:

```bash
gcloud auth application-default login
```

These credentials allow the Python application to access Cloud Storage without storing a service account key in the repository.

### Step 6: Test the data processing

Run:

```bash
python process_data.py
```

This retrieves historical weather data and displays the processed summary in the terminal.

### Step 7: Run the pipeline through the ADK agent

Run:

```bash
python run_agent.py
```

The Gemini-powered agent should invoke `run_weather_pipeline()`.

The tool processes the weather data and uploads `weather_summary.json` to the configured Google Cloud Storage bucket.

The terminal displays the tool execution and the agent's final summary.

### Step 8: Run the pipeline directly (optional)

The pipeline can also be tested without the AI agent:

```bash
python storage.py
```

This is useful for testing API ingestion, data processing, and Google Cloud Storage independently.

### Step 9: Launch the dashboard

After successfully uploading the processed results, run:

```bash
python app.py
```

Open the following URL in your browser:

http://127.0.0.1:5000

The Flask application retrieves the stored JSON file and displays the weather statistics and visualizations.

**Note:** The dashboard runs locally and requires access to the configured private Google Cloud Storage bucket. It is not publicly hosted.

## Example Results

The pipeline was tested using Bloomington, Indiana, weather observations from October 1–7, 2025.

| Metric | Result |
|---|---|
| Average daily maximum temperature | 27.3°C |
| Total precipitation | 38.4 mm |
| Number of days analyzed | 7 |
| Cloud storage output | `weather_summary.json` |

## Security and Credentials

The project uses a private Google Cloud Storage bucket.

Google Cloud Application Default Credentials are used to authenticate the Python application locally.

The `.gitignore` file excludes sensitive and unnecessary local files, including:

- `.env`
- `.venv/`
- Python cache files
- Google Cloud credential files

API keys and authentication credentials are not included in the public repository.

## Limitations

- The current pipeline analyzes one city and a fixed historical date range.
- The agent initiates a predefined Python pipeline through a single ADK function tool.
- The workflow is manually triggered rather than scheduled.
- The dashboard is hosted locally rather than deployed publicly.
- Cloud Storage access requires a configured Google Cloud project, bucket, and appropriate permissions.

## Future Improvements

A separate **Future Improvements PDF** accompanies the Canvas submission.

It discusses potential enhancements such as automated scheduling, additional locations and analysis periods, improved error handling and monitoring, and more advanced analytics and visualizations.

## Data Source

Open-Meteo Historical Weather API:

https://open-meteo.com/en/docs/historical-weather-api

## Repository

https://github.com/atmikha/weather-insights-ai
