
import pandas as pd
from api import get_weather_data


def process_weather_data():
    """Clean and summarize Bloomington weather data."""

    weather = get_weather_data()

    # Convert the API response into a pandas DataFrame.
    df = pd.DataFrame(weather["daily"])

    # Remove rows with missing weather values.
    df = df.dropna(
        subset=["time", "temperature_2m_max", "precipitation_sum"]
    ).copy()

    # Convert dates and ensure chronological order.
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time")

    # Filter the observations to the requested period.
    start_date = pd.Timestamp("2025-10-01")
    end_date = pd.Timestamp("2025-10-07")

    df = df[
        (df["time"] >= start_date)
        & (df["time"] <= end_date)
    ].copy()

    if df.empty:
        raise ValueError("No weather data available for this period.")

    # Categorize days so they can be grouped.
    df["weather_type"] = df["precipitation_sum"].apply(
        lambda rain: "Rainy" if rain > 0 else "Dry"
    )

    # Aggregate statistics across all days.
    average_temp = round(float(df["temperature_2m_max"].mean()), 2)
    total_rain = round(float(df["precipitation_sum"].sum()), 2)

    # Group and aggregate by rainy versus dry days.
    grouped = (
        df.groupby("weather_type")
        .agg(
            number_of_days=("time", "count"),
            average_max_temperature=("temperature_2m_max", "mean"),
            total_precipitation=("precipitation_sum", "sum"),
        )
        .reset_index()
    )

    weather_groups = []

    for _, row in grouped.iterrows():
        weather_groups.append({
            "weather_type": str(row["weather_type"]),
            "number_of_days": int(row["number_of_days"]),
            "average_max_temperature": round(
                float(row["average_max_temperature"]), 2
            ),
            "total_precipitation": round(
                float(row["total_precipitation"]), 2
            ),
        })

    # Keep daily observations for dashboard charts.
    daily_data = []

    for _, row in df.iterrows():
        daily_data.append({
            "date": row["time"].strftime("%Y-%m-%d"),
            "max_temperature": float(row["temperature_2m_max"]),
            "precipitation": float(row["precipitation_sum"]),
            "weather_type": str(row["weather_type"]),
        })

    summary = {
        "location": "Bloomington, Indiana",
        "start_date": "2025-10-01",
        "end_date": "2025-10-07",
        "temperature_unit": "C",
        "precipitation_unit": "mm",
        "average_max_temperature": average_temp,
        "total_precipitation": total_rain,
        "number_of_days": int(len(df)),
        "weather_groups": weather_groups,
        "daily_data": daily_data,
    }

    return summary


if __name__ == "__main__":
    import json

    print(json.dumps(process_weather_data(), indent=2))
