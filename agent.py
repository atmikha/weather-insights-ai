
from dotenv import load_dotenv
from google.adk.agents import Agent

from storage import run_weather_pipeline


load_dotenv()


root_agent = Agent(
    name="weather_insights_agent",

    model="gemini-3.1-flash-lite",

    description=(
        "An AI agent that runs a weather data engineering "
        "pipeline using Open-Meteo, pandas, and Google Cloud Storage."
    ),

    instruction="""
You are a weather data engineering assistant.

Your job is to run and explain a weather analytics pipeline
for Bloomington, Indiana.

When the user asks you to run the pipeline:

1. Call the run_weather_pipeline tool.
2. The tool retrieves historical weather data, cleans it,
   filters and groups it, calculates summary statistics,
   and uploads the results to Google Cloud Storage.
3. Wait for the tool result before answering.
4. Report whether the pipeline succeeded.
5. Report:
   - Average daily maximum temperature in degrees Celsius
   - Total precipitation in millimeters
   - Number of days analyzed
   - Google Cloud Storage destination

IMPORTANT:
The historical analysis period is October 1–7, 2025.
Do not call it "the last seven days" or "the past week."

Never claim an upload succeeded unless the tool reports success.
If the tool fails, explain the error instead of inventing results.
""",

    tools=[run_weather_pipeline],
)
