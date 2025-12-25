from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.planners import BuiltInPlanner
from google.genai import types
# from google.adk.tools import google_search  # Import the search tool
from .tools import (
    create_event,
    delete_event,
    edit_event,
    get_current_time,
    list_events,
    spotify,
    file_system,
    browser
)

root_agent = Agent(
    # A unique name for the agent.
    name="jarvis",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        ),
    description="Agent to help with scheduling and calendar, and Spotify operations.",
    instruction=f"""
    You are Jarvis, an AI assistant integrated with Google Calendar and Spotify. You can help users manage their calendar events and control their Spotify music playback. Use the provided tools to perform actions as needed. You can also interact with the file system to manage files and directories.
    You have a playful and friendly personality. 

    you can use browser tool to access web pages when needed.
    This is your allowed directory for file system operations: {file_system.TARGET_FOLDER_PATH}
    You should not ask the user for information that you can retrieve yourself. 
    Today's date is {get_current_time()}.
    """,
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024
        )
    ),
    tools=[
        list_events,
        create_event,
        edit_event,
        delete_event,
        spotify._mcp,
        file_system._mcp,
        browser._mcp
    ],
)
