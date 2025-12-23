from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os
from datetime import datetime, timedelta

# Read last stored time from file
time_file = "time.txt"
current_time = datetime.now()
try:
    with open(time_file, "r") as f:
        last_time = datetime.fromisoformat(f.read().strip())
        if last_time - current_time > timedelta(hours=6):
            os.system("cd D:/Programming/AI/ADK AGENTS/spotify-mcp-server && npm run auth")
except FileNotFoundError:
    with open(time_file, "w") as f:
        f.write(current_time.isoformat())


spotify_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='node',
            args=[
                "D:/Programming/AI/ADK AGENTS/spotify-mcp-server/build/index.js"
            ],
        )
    )
)