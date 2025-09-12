import asyncio
from pprint import pprint

import boto3
from botocore.config import Config
from langchain_aws import ChatBedrock
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


def get_llm():
    llm = ChatBedrock(
        client=boto3.client(
            'bedrock-runtime',
            region_name='us-east-1',
            config=Config(
                read_timeout=1000,
                retries={'max_attempts': 3}
            )
        ),
        model_kwargs={
            "max_tokens": 4000,
            "temperature": 0.1,
            "top_p": 0.9
        },
        model='us.anthropic.claude-3-7-sonnet-20250219-v1:0'
    )
    return llm


async def setup_mcp_client():
    """Initialize a MultiServerMCPClient with the provided server configuration."""
    client = MultiServerMCPClient({
        "servers":
            {
                "command": "uv",
                "args": ["run", "/Users/vinodkumarkp/PycharmProjects/basic_agent_demo/basic_mcp_server.py"],
                "transport": "stdio"
            }
    })

    tools = await client.get_tools()
    return tools


async def initialize_agent():
    llm = get_llm()
    tools = await setup_mcp_client()
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a helpful AI assistant that helps people find information. Use the tools below to answer the question as best you can. If you don't know the answer, just say that you don't know. Do not try to make up an answer."
    )
    return agent

async def run_agent(agent):
    async for chunk in agent.astream({"messages": [{"role": "user", "content": "List all the dummy names?"}]}):
        pprint(chunk)


agent = asyncio.run(initialize_agent())
asyncio.run(run_agent(agent))



