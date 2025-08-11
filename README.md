# GitLab AI Bug-Fixer 

This project provides a powerful framework for automating GitLab workflows using an AI agent. It features a Model-Context-Protocol (MCP) server with tools for standard GitLab API interactions (reading/writing files, creating issues) and a custom tool that leverages a Large Language Model (LLM) to automatically fix bugs in code.

The key innovation is the use of the mcp_use library, which creates a standalone agent. This allows you to interact with the MCP server directly from a Python script, bypassing the need for integrated platforms like VS Code plugins or specific desktop applications.

## How It Works

The architecture consists of several components working in tandem:

- The Agent (`demo.py`): A Python script using the mcp_use library and langchain-together to define a task (e.g., "Fix this bug in this code"). It acts as the brain, sending the request to the MCP server.

- The MCP Server (`index.js`): A Node.js server that exposes a set of tools to the agent. It listens for tool calls and executes the corresponding action.

- GitLab API Tools: Standard tools built into the MCP server for common tasks like `get_file_contents` and `create_or_update_file`.

- Custom Bug-Fix Tool: The `fix_bug_in_code` tool is a custom addition. When called by the agent, the MCP server makes an HTTP request to a separate Python API.

- The Bug-Fix API (`py_api.py`): A Flask-based web server that receives the code snippet, language, and bug description. It uses the Together.ai API to query a powerful code model (Qwen/Qwen2.5-Coder-32B-Instruct) to generate the corrected code.

The workflow is as follows:  
User Prompt -> Agent (`demo.py`) -> MCP Server (`index.js`) -> Bug-Fix API (`py_api.py`) -> Together AI

## Features

- GitLab Automation: Programmatically interact with GitLab repositories.

  - Create, read, and update files (`create_or_update_file`, `get_file_contents`).

  - Manage repositories (`search_repositories`, `create_repository`, `fork_repository`).

  - Manage branches, issues, and merge requests.

- AI-Powered Bug Fixing: Automatically correct bugs in code snippets using the `fix_bug_in_code` tool.

- Standalone Agent: Run complex workflows from a simple Python script without dependency on external agent platforms.

## Prerequisites

- Node.js: To run the MCP server.

- Python 3.7+: To run the Bug-Fix API and the demo agent.

- GitLab Personal Access Token: With api scope.

- Together AI API Key: To use the code-fixing LLM.

## Installation & Setup 🛠️

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```
2. Install Node.js dependencies for the MCP server:

```bash
# In the root directory
npm install
```
3. Install Python dependencies for the API and agent. It's recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate
pip install Flask together "mcp_use[all]" langchain-together
```
Configure Environment:

    1. In index.js, ensure the path to your Node.js executable and the script are correct.

    2. In demo.py, add your GitLab Personal Access Token to the config dictionary.

    3. In py_api.py, add your Together AI API key where it says client = Together(api_key="...").


