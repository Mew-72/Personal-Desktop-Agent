from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
import os
from datetime import datetime, timedelta

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