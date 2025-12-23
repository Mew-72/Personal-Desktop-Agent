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
    file_system
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
    You have a playful and friendly personality. You must do what you are told without askinging questions.
    Today's date is {get_current_time()}.
    """,
    tools=[
        list_events,
        create_event,
        edit_event,
        delete_event,
        spotify.spotify_mcp,
        file_system.file_mcp,
    ],
    # tools=[]
)
