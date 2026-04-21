import asyncio
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0.9, max_tokens=2048)

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/roland/Documents/Projects/mcp-crash-course/servers/math_server.py"],
    )

async def main():
    print("Hello from mcp-crash-course!")

    async with stdio_client(stdio_server_params) as (read,write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Client session initialized")

            tools = await load_mcp_tools(session)
            print(f"Loaded tools: {tools}")

            agent = create_agent(llm,tools)
            print("Agent created")

            result = await agent.ainvoke({"messages": [HumanMessage(content="What is 54 + 2 * 3?")]})
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
