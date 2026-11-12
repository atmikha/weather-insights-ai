
from flask import Flask, render_template

from storage import get_stored_weather_data


app = Flask(__name__)


@app.route("/")
def dashboard():
    """Display weather analytics stored in Google Cloud."""

    try:
        weather = get_stored_weather_data()

        return render_template(
            "index.html",
            weather=weather,
            error=None,
        )

    except Exception as exc:
        print(f"Dashboard error: {exc}")

        return render_template(
            "index.html",
            weather=None,
            error=(
                "Could not load the weather data from Google Cloud "
                "Storage. Run the weather pipeline first and "
                "check your Google Cloud credentials."
            ),
        ), 503


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
