
import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from agent import root_agent


load_dotenv()


async def main():
    runner = InMemoryRunner(
        app_name="weather_insights_app",
        agent=root_agent,
    )

    session = await runner.session_service.create_session(
        app_name="weather_insights_app",
        user_id="student",
    )

    message = types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=(
                    "Run the complete historical weather pipeline "
                    "for Bloomington, Indiana, for October 1–7, 2025. "
                    "Process the observations, upload the results to "
                    "Google Cloud Storage, and summarize the outcome."
                )
            )
        ],
    )

    print("Starting Weather Insights AI agent...\n")

    async for event in runner.run_async(
        user_id="student",
        session_id=session.id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.function_call:
                    print(
                        f"\nAgent called tool: "
                        f"{part.function_call.name}"
                    )

                if part.function_response:
                    print(
                        f"Tool completed: "
                        f"{part.function_response.name}"
                    )

                if part.text and event.author == root_agent.name:
                    print(f"\nAgent response:\n{part.text}")


if __name__ == "__main__":
    asyncio.run(main())
