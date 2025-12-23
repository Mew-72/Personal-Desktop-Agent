import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.adk.agents.run_config import RunConfig
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from pydantic import BaseModel
from jarvis.agent import root_agent

#
# ADK Streaming
#

# Load Gemini API Key
load_dotenv()

APP_NAME = "ADK Streaming example"
session_service = InMemorySessionService()
sessions_cache = {}  # Cache for active sessions


async def start_agent_session(session_id):
    """Starts an agent session for text-based interaction"""

    # Create a Session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=session_id,
        session_id=session_id,
    )

    # Create a Runner
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Create run config for text-only responses (non-streaming)
    run_config = RunConfig(response_modalities=["TEXT"])

    # Return runner and session for use in message endpoint
    return runner, session, run_config


async def collect_agent_response(
    events,
) -> str:
    """Collect the complete agent response from events"""
    response_text = ""
    # Process the async generator
    async for event in events:
        print(event) # only for debugging
        if event is None:
            continue

        # If the turn is complete, we're done
        if event.turn_complete:
            print(f"[AGENT]: Turn complete")
            break

        # Read all parts from the Content, not just the first one
        if not event.content or not event.content.parts:
            continue
            
        for part in event.content.parts:
            if not part:
                continue

            # Make sure we have a valid Part
            if not isinstance(part, types.Part):
                continue

            # Collect text responses from all parts
            if part.text:
                response_text += part.text
                print(f"[AGENT TO CLIENT]: {part.text}")
    
    return response_text


#
# FastAPI web app
#

class MessageRequest(BaseModel):
    """Request model for message endpoint"""
    message: str
    session_id: str | None = None

app = FastAPI()

STATIC_DIR = Path("static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serves the index.html"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/api/message")
async def message_endpoint(request: MessageRequest):
    """HTTP endpoint for sending messages to the agent"""
    
    # Use provided session ID or generate a new one
    session_id = request.session_id or f"session_{base64.b64encode(os.urandom(8)).decode()}"
    
    print(f"[SESSION]: {session_id}")
    print(f"[CLIENT TO AGENT]: {request.message}")
    
    try:
        # Get or create agent session for this conversation
        if session_id in sessions_cache:
            runner, session, run_config = sessions_cache[session_id]
            print(f"[SESSION]: Reusing existing session")
        else:
            runner, session, run_config = await start_agent_session(session_id)
            sessions_cache[session_id] = (runner, session, run_config)
            print(f"[SESSION]: Created new session")
        
        # Create the user message content
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=request.message)]
        )
        # user_content = request.message
        
        # Run the agent with request/response (async version for FastAPI compatibility)
        events = runner.run_async(
            session_id=session_id,
            user_id=session.user_id,
            new_message=user_content,
            run_config=run_config,
        )
        
        # Collect the complete response from the agent
        response_text = await collect_agent_response(events)
        
        # Return the response
        return {
            "response": response_text,
            "message": response_text  # Include both keys for flexibility
        }
    
    except Exception as e:
        print(f"[ERROR]: {e}")
        return {
            "response": f"Error: {str(e)}",
            "message": f"Error: {str(e)}"
        }
