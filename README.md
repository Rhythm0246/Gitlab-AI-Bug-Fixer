# GitLab AI Bug-Fixer

This project provides a powerful framework for automating GitLab workflows using an AI agent. It features a **Model-Context-Protocol (MCP) server** with tools for standard GitLab API interactions (reading/writing files, creating issues) and a custom tool that leverages a Large Language Model (LLM) to **automatically fix bugs in code**.

The key innovation is the use of the `mcp_use` library, which creates a standalone agent. This allows you to interact with the MCP server directly from a Python script, bypassing the need for closed-source agents like copilot,claude desktop.

-----

## How It Works

The architecture consists of several components working in tandem:

1. **The Agent (`demo.py`)**: A Python script using the `mcp_use` library and `langchain-together` to define a task (e.g., "Fix this bug in this code"). It acts as the brain, sending the request to the MCP server.

2. **The MCP Server (`index.js`)**: A Node.js server that exposes a set of tools to the agent. It listens for tool calls and executes the corresponding action.

3. **GitLab API Tools**: Standard tools built into the MCP server for common tasks like `get_file_contents` and `create_or_update_file`.

4. **Custom Bug-Fix Tool**: The `fix_bug_in_code` tool is a custom addition. When called by the agent, the MCP server makes an HTTP request to a separate Python API.

5. **The Bug-Fix API (`py_api.py`)**: A Flask-based web server that receives the code snippet, language, and bug description. It uses the Together.ai API to query a powerful code model (`Qwen/Qwen2.5-Coder-32B-Instruct`) to generate the corrected code.

The workflow is as follows:  
`User Prompt` → `Agent (demo.py)` → `MCP Server (index.js)` → `Bug-Fix API (py_api.py)` → `Together AI`

-----

## Features

- **GitLab Automation**: Programmatically interact with GitLab repositories.
  - Create, read, and update files (`create_or_update_file`, `get_file_contents`).
  - Manage repositories (`search_repositories`, `create_repository`, `fork_repository`).
  - Manage branches, issues, and merge requests.
- **AI-Powered Bug Fixing**: Automatically correct bugs in code snippets using the `fix_bug_in_code` tool.
- **Standalone Agent**: Run complex workflows from a simple Python script without dependency on external agent platforms.

-----

## Prerequisites

- **Node.js**: To run the MCP server.
- **Python 3.7+**: To run the Bug-Fix API and the demo agent.
- **GitLab Personal Access Token**: With `api` scope.
- **Together AI API Key**: To use the code-fixing LLM.

-----

## Installation & Setup

1. **Clone the repository**:

    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2. **Install Node.js dependencies** for the MCP server:

    ```bash
    # In the root directory
    npm install
    ```

3. **Install Python dependencies** for the API and agent. It's recommended to use a virtual environment.

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install Flask together "mcp_use[all]" langchain-together
    ```

4. **Configure Environment**:

    - In `index.js`, ensure the path to your Node.js executable and the script are correct.
    - In `demo.py`, add your GitLab Personal Access Token to the `config` dictionary.
    - In `py_api.py`, add your Together AI API key where it says `client = Together(api_key="...")`.

-----

## Usage

The system requires two components to be running.

1. **Start the Bug-Fix API Server**:  
   Open a terminal and run the Flask app. This will host the `/fix` endpoint locally.

    ```bash
    python3 py_api.py
    ```

2. **Run the Agent**:  
   Open a *second terminal* and run the demo script. This script will automatically start the MCP server and execute the prompt.

    ```bash
    python3 demo.py
    ```

-----

## Example Session

Running `python3 demo.py` will produce the following output, showing the agent calling the `fix_bug_in_code` tool and returning the corrected code snippet.

````text
$ python3 demo.py
Enter your Together API key:
2025-08-11 16:15:50,346 - mcp_use - INFO - 🧠 Agent ready with tools: create_or_update_file, search_repositories, create_repository, get_file_contents, push_files, create_issue, create_merge_request, fork_repository, create_branch, fix_bug_in_code
2025-08-11 16:15:50,388 - mcp_use - INFO - ✨ Agent initialization complete
2025-08-11 16:15:50,388 - mcp_use - INFO - 💬 Received query: ' I have a bug in the following code snippet writte...'
2025-08-11 16:15:50,388 - mcp_use - INFO - 🏁 Starting agent execution with max_steps=30
2025-08-11 16:15:50,388 - mcp_use - INFO - 👣 Step 1/30
2025-08-11 16:16:36,103 - mcp_use - INFO - 🔧 Tool call: fix_bug_in_code with input: {'bug_description': 'Function arguments should be passed only once', 'file_content': 'def add(x, ...
2025-08-11 16:16:36,104 - mcp_use - INFO - 📄 Tool result: {   "status": "success",   "fixed_code": "def add(x, y):\n    return x + y\n\n\ndef multiply(x, y...}
2025-08-11 16:16:36,104 - mcp_use - INFO - 👣 Step 2/30
2025-08-11 16:16:50,944 - mcp_use - INFO - ✅ Agent finished at step 2
2025-08-11 16:16:50,944 - mcp_use - INFO - 🎉 Agent execution complete in 60.78 seconds

Result12: The corrected code snippet is:
```python
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def say_hello(name):
    print(f"Hello, {name}!")

def call_with_duplicate_args():
    result = add(10, 5)  
    print("Result:", result)

if __name__ == "__main__":
    print("Addition:", add(3, 4))
    print("Multiplication:", multiply(3, 4))
    say_hello("Anish")
````
## Future Works

Sophisticated agents, such as GitHub Copilot integrated into an IDE, can perform **incremental tool calls**, chaining multiple tools together to resolve a complex request.
An example of the desired future workflow for the standalone agent:

1. **User Prompt**: "Fix the bug in `test.py` in the project `blanketcoder/dummy`."
2. **Tool Call 1**: Agent decides to call `get_file_contents` for `test.py`.
3. **Tool Call 2**: Agent uses the retrieved content to call `fix_bug_in_code`.
4. **Tool Call 3**: Agent takes the fixed code and calls `create_or_update_file` to write it back to GitLab.
```

