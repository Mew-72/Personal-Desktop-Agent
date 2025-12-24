from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os

# load environment variables from .env file in the root directory of the project
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

_mcp = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='node',
            args=[
                os.environ.get("SPOTIFY_MCP_PATH")
            ],
        )
    )
)