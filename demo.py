import getpass
import os
import asyncio
import os
import os
from mcp_use import MCPAgent, MCPClient
from langchain_together import ChatTogether
import mcp_use
async def main():
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your Together API key: ")

    llm = ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        temperature=0,
    )
    config = {
    "mcpServers": {
        "gitlab": {
            "command": "/home/blanketcoder/.nvm/versions/node/v22.17.0/bin/node",
            "args": [
                "/home/blanketcoder/mcp/node_modules/@modelcontextprotocol/server-gitlab/dist/index.js"
            ],
            "env": {
                "GITLAB_PERSONAL_ACCESS_TOKEN": "Enter your gitlab token",
                "GITLAB_API_URL": "https://gitlab.com/api/v4"
            }
        }
    }
}

    client = MCPClient.from_dict(config)
    agent = MCPAgent(llm=llm, client=client, max_steps=30, verbose=False)

    try:
        result = await agent.run(
    """
I have a bug in the following code snippet written in Python. The bug is:
"Function arguments should be passed only once".

Here is the code snippet:

def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def say_hello(name):
    print(f"Hello, {name}!")

def call_with_duplicate_args():
    result = add(10, x=5)  
    print("Result:", result)

if __name__ == "__main__":
    print("Addition:", add(3, 4))
    print("Multiplication:", multiply(3, 4))
    say_hello("Anish")
Fix the bug and give me the corrected code.
"""
)
        print(f"\nResult12: {result}")
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
