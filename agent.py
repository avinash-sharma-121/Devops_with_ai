from strands import Agent, tool
from strands_tools import calculator, http_request
from strands.models.ollama import OllamaModel
from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient

# add tools
from tools import about_me, run_shell, get_time, disk_usage, kubectl_get_pods,get_weather,random_number

from tools_pdf import read_pdf,generate_pdf

#define local model
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen2.5:1.5b"
)

# MCP Server configuration - FastMCP SSE endpoint
MCP_SERVER_URL = "http://localhost:8000/sse"

# Create MCP client with SSE transport for FastMCP
streamable_http_mcp_client = MCPClient(
    lambda: sse_client(MCP_SERVER_URL)
)

system_prompt = "You are a helpful assistant."\
      "you give answers in a kind and informative manner."\
        "you can use correct data sources to answer the user's question."\
          "you can use the tools and free apis to get the correct answer for the user."\
            "if you don't know the answer, you can say you don't know instead of making up an answer."\
            "if we are mentioning a word like pdf for read and generate pdf, you can use the tools provided to read and generate pdfs."\
            "if we are mentioning a word like weather, you can use the tools provided to get the weather information."\
            "if we are mentioning a word like time, you can use the tools provided to get the current system time."\
            "if we are mentioning a word like disk usage, you can use the tools provided to get the current disk usage."\
            "if we are mentioning a word like kubernetes pods, you can use the tools provided to get the current kubernetes pods information."\
            "if we are mentioning a word like random number, you can use the tools provided to generate a random number between 1 and 100."\
            "always try to use the tools provided to get the correct answer for the user."\
            "if the user is asking for a calculation, you can use the calculator tool to get the correct answer."\
            "if the user is asking for a http request, you can use the http_request tool to get the correct answer."\
            "if the user is asking for a pdf related question, you can use the read_pdf and generate_pdf tools to get the correct answer."

try:
    print("🔗 Connecting to MCP Server at", MCP_SERVER_URL)
    try:

        with streamable_http_mcp_client:
            print("✓ Connected to MCP Server")
            tools = streamable_http_mcp_client.list_tools_sync()
            print(f"✓ Retrieved {len(tools)} tools from MCP Server")

            agent = Agent(model=ollama_model,
                          tools=tools,
                          system_prompt=system_prompt)
            print(f"✓ Agent initialized")
            print("\n📊 Available tools from MCP Server:")
            for i, tool_item in enumerate(tools, 1):
                # MCPAgentTool has tool_name attribute
                tool_name = getattr(tool_item, 'tool_name', f'Tool {i}')
                print(f"   {i}. {tool_name}")

            print(f"\n{'='*60}")
            user_input = input("What do you want to ask the agent? ")
            if user_input.strip():
                print(f"\n🤖 Processing: {user_input}\n")
                agent(user_input)
            else:
                print("No input provided. Exiting.")

    except Exception as e:
        print(f"\n❌ Error during MCP Server connection or tool retrieval: {e}")
        print("\n📌 Please ensure the MCP server is running and accessible at http://localhost:8000/sse")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n📌 MCP Server Connection Failed")
    print(f"   Trying to connect to: {MCP_SERVER_URL}")
    print("\n   Make sure the MCP server is running at http://127.0.0.1:8000/sse")
    import traceback
    traceback.print_exc()
