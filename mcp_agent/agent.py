from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters
)
import os
from dotenv import load_dotenv
import opik
from opik.integrations.adk import OpikTracer

# Load environment variables from .env file
load_dotenv()

# Initialize and configure Opik tracer
opik.configure(use_local=False)
tracer = OpikTracer()

# Set up Google Maps API key from environment variable
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_PLATFORM_API_KEY")

# Intialize Agent using OpenAI's GPT-4o
root_agent = LlmAgent(
    model=LiteLlm(
        model="openai/gpt-4o"
    ),
    name="openai_agent",
    description=(
        "An intelligent mapping assistant that provides driving, walking, and "
        "public transportation directions between cities or landmarks. "
        "The assistant can estimate travel times and distances, suggest "
        "optimal routes, and help users understand geographic relationships "
        "between locations."
    ),
    instruction=(
        "When the user asks for routes, travel times, or directions between "
        "locations, use the mapping tool to fetch detailed and accurate "
        "navigation information. Respond clearly with turn-by-turn steps, "
        "estimated time, and mode of transport when available. If the user "
        "asks which place is closer or farther, or for cities near a specific "
        "location, use the mapping tool to reason geographically."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps"
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
                },
            ),
        )
    ],
    # Setting up tracing for observability
    before_agent_callback=tracer.before_agent_callback,
    after_agent_callback=tracer.after_agent_callback,
    before_model_callback=tracer.before_model_callback,
    after_model_callback=tracer.after_model_callback,
    before_tool_callback=tracer.before_tool_callback,
    after_tool_callback=tracer.after_tool_callback,
)
