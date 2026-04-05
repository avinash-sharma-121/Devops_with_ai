#!/usr/bin/env python3
"""
Debug script to inspect MCPAgentTool structure
"""

from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient

MCP_SERVER_URL = "http://localhost:8000/sse"

streamable_http_mcp_client = MCPClient(
    lambda: sse_client(MCP_SERVER_URL)
)

print("Inspecting MCPAgentTool structure...")
print("=" * 60)

try:
    with streamable_http_mcp_client:
        tools = streamable_http_mcp_client.list_tools_sync()
        
        for i, tool in enumerate(tools, 1):
            print(f"\n🔧 Tool {i}:")
            print(f"   Type: {type(tool)}")
            
            # Show tool_name directly
            if hasattr(tool, 'tool_name'):
                print(f"   ✓ tool_name: {tool.tool_name}")
            
            # Show other useful attributes
            if hasattr(tool, 'tool_spec'):
                print(f"   tool_spec: {tool.tool_spec}")
            
            if hasattr(tool, 'mcp_tool'):
                print(f"   mcp_tool: {tool.mcp_tool}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

