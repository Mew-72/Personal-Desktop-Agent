# Personal Desktop Agent (Jarvis)

A local, privacy-focused AI assistant engineered with **Google's Agent Development Kit (ADK)** and the **Model Context Protocol (MCP)**. This agent unifies cloud services (Google Calendar) and local desktop control (Spotify, Filesystem) into a single natural language interface served via **FastAPI**.

## 🚀 Features

* **📅 Calendar Orchestration:** Full bi-directional sync with Google Calendar. The agent can list, create, edit, and delete events using complex natural language queries (e.g., *"Move my meeting with John to next Tuesday at 2 PM"*).
* **🎵 Spotify Control (MCP):** Integrated via the **Model Context Protocol**, allowing the agent to control playback, search tracks, and manage queues by communicating directly with a local Node.js MCP server.
* **📂 File System Access:** Safe interaction with the local file system to read/write logs or documents upon request.
* **⚡ Real-time Interface:** A reactive chat UI built with **JavaScript (ES6)** and **FastAPI**, featuring streaming responses and persistent conversation memory.

## 🏗️ Architecture & Roadmap

### Current Architecture (v1.0)
The system currently runs as a **Single-Agent Orchestrator** using Google's ADK.
* **Core:** `gemini-2.5-flash-lite` (Router & Planner)
* **Calendar:** Custom Python Tool (Google API)
* **Music:** Integrated via [spotify-mcp-server](https://github.com/marcelmarais/spotify-mcp-server) (Lightweight Node.js MCP)
* **Files:** Native MCP Filesystem integration

### Roadmap (v2.0 - In Progress)
I am currently refactoring the system into a **Multi-Agent Swarm**:
* [ ] **Research Agent:** Porting my [Reddit Intelligence Bot](https://github.com/Mew-72/reddit-bot) into an MCP tool to allow the agent to "browse" and summarize social trends on command.
* [ ] **System Agent:** Dedicated sub-agent for file operations and OS-level command execution.
* [ ] **Voice Mode:** Implementing WebSocket-based audio streaming for real-time voice interaction.
* [ ] **Docker Support:** Containerizing the stack for easy deployment.

## 📂 Project Structure

```text
personal-desktop-agent/
├── app/
│   ├── jarvis/
│   │   ├── agent.py           # Agent definition & instructions
│   │   └── tools/             # Tool definitions (Calendar, MCP connectors)
│   ├── static/                # Frontend assets (HTML, CSS, JS)
│   └── main.py                # FastAPI entry point & Session Management
├── credentials.json           # Google OAuth Client Secret (Not in repo)
├── setup_calendar_auth.py     # OAuth2.0 Token Generator script
└── requirements.txt           # Python dependencies
```

## ⚙️ Setup & Installation

### Prerequisites

* Python 3.10+
* Node.js (for running MCP servers)
* A Google Cloud Project with **Calendar API** enabled.

### 1. Clone & Install

```bash
git clone https://github.com/Mew-72/Personal-Desktop-Agent
cd personal-desktop-agent
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```ini
GOOGLE_API_KEY=your_gemini_api_key
# Path to your local Spotify MCP server build
SPOTIFY_MCP_PATH=./path/to/spotify-mcp-server/index.js
```

### 3. Google Calendar Auth

1. Place your `credentials.json` (from Google Cloud Console) in the root folder.
2. Run the authentication script to generate your token:
```bash
python setup_calendar_auth.py
```



### 4. Running the Agent

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to interact with Jarvis.

## Model Context Protocol (MCP) Details

This project demonstrates the power of **MCP** to decouple the agent's logic from tool implementation.

* The **Spotify Tool** connects to a local Node.js process via standard input/output (Stdio).
* This allows the Python agent to control a JavaScript-based Spotify controller without complex cross-language bindings.

## 👤 Author

**Mayank Kumar**