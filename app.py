#!/usr/bin/env python3
"""
FastAPI Backend for DevOps AI Agent
Provides REST API endpoints for the AI agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import logging
from typing import List, Optional
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import agent and tools
from strands import Agent
from strands.models.ollama import OllamaModel
from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient

# Import all tools
from tools import about_me, run_shell, get_time, disk_usage, kubectl_get_pods, get_weather, random_number
from tools_pdf import read_pdf, generate_pdf


# FastAPI app
app = FastAPI(
    title="DevOps AI Agent API",
    description="REST API for the DevOps AI Agent",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# Pydantic Models
# ========================

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List] = None

class ToolInfo(BaseModel):
    name: str
    description: str

class AgentStatus(BaseModel):
    status: str
    tools_count: int
    model: str
    mcp_connected: bool

# ========================
# Initialize Agent
# ========================

agent = None
mcp_client = None
mcp_connected = False
tools_list = []

def initialize_agent():
    """Initialize the agent with all tools"""
    global agent, mcp_connected, tools_list, mcp_client
    
    logger.info("🤖 Initializing agent...")
    
    # Setup Ollama model
    ollama_model = OllamaModel(
        host="http://localhost:11434",
        model_id="qwen2.5:1.5b"
    )
    
    # Try to connect to MCP
    mcp_tools = []
    try:
        logger.info("🔌 Connecting to CustomFastMCP...")
        MCP_SERVER_URL = "http://localhost:8000/sse"
        # Create MCP client - will be used as context manager in chat endpoints
        mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))
        # Use context to get tools, then exit
        with mcp_client:
            mcp_tools = mcp_client.list_tools_sync()
        mcp_connected = True
        logger.info(f"✅ FastMCP connected! Found {len(mcp_tools)} tools")
    except Exception as e:
        logger.warning(f"⚠️  FastMCP not available: {str(e)}")
        mcp_connected = False
        mcp_client = None
    
    # Combine all tools
    all_tools = []
    
    # Add MCP tools
    if mcp_tools:
        all_tools.extend(mcp_tools)
    
    # Add system tools
    local_tools_list = [
        about_me, run_shell, get_time, disk_usage, kubectl_get_pods, random_number, read_pdf, generate_pdf
    ]
    all_tools.extend(local_tools_list)
    
    # Store tools list for API
    tools_list = all_tools
    
    system_prompt = """You are a helpful DevOps assistant with expertise in:

📦 CUSTOM TOOLS (from FastMCP):
- add_numbers: Perform mathematical calculations
- get_forecast: Get weather forecasts
- get_alerts: Get weather alerts

🔧 SYSTEM & LOCAL TOOLS:
- run_shell: Execute shell commands
- get_time: Get current time
- disk_usage: Check disk usage
- get_weather: Get weather information
- random_number: Generate random numbers
- read_pdf, generate_pdf: PDF operations
- about_me: Get info about the assistant
- kubectl_get_pods: Get Kubernetes pods info

IMPORTANT:
- Use custom tools for calculations and data from FastMCP
- Use system tools for general operations
- Always provide clear, concise responses
- Offer helpful suggestions based on user queries
"""
    
    # Create agent
    agent = Agent(
        model=ollama_model,
        #model="anthropic.claude-3-haiku-20240307-v1:0",
        tools=all_tools,
        system_prompt=system_prompt
    )
    
    logger.info(f"✅ Agent initialized with {len(all_tools)} tools")
    return agent

# Initialize agent on startup
@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    global agent, mcp_connected, tools_list
    try:
        agent = initialize_agent()
    except Exception as e:
        logger.error(f"Failed to initialize agent: {str(e)}")

# ========================
# API Endpoints
# ========================

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return html_path
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint - send message to agent and get response
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        logger.info(f"Processing: {request.message[:100]}")
        
        # Use MCP client context manager for each request
        if mcp_client:
            with mcp_client:
                response = agent(request.message)
        else:
            response = agent(request.message)
        
        # Extract the message text from the structured response
        try:
            # Response structure: {message: {content: [{text: "..."}]}}
            if isinstance(response, dict) and 'message' in response:
                message_obj = response['message']
                if isinstance(message_obj, dict) and 'content' in message_obj:
                    content_list = message_obj['content']
                    if isinstance(content_list, list) and len(content_list) > 0:
                        text_content = content_list[0]
                        if isinstance(text_content, dict) and 'text' in text_content:
                            response_text = text_content['text']
                        else:
                            response_text = str(content_list[0])
                    else:
                        response_text = str(response)
                else:
                    response_text = str(response)
            else:
                response_text = str(response)
        except Exception as parse_error:
            logger.warning(f"Could not parse response: {parse_error}")
            response_text = str(response)
        
        return {
            "success": True,
            "response": response_text,
            "message": request.message
        }
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/chat/stream")
async def chat_stream(message: str):
    """
    Streaming chat endpoint - returns response as server-sent events
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    async def event_generator():
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'message': message})}\n\n"
            
            # Get response from agent
            logger.info(f"Streaming: {message[:100]}")
            
            # Use MCP client context manager for each request
            if mcp_client:
                with mcp_client:
                    response = agent(message)
            else:
                response = agent(message)
            
            # Extract the message text from the structured response
            try:
                if isinstance(response, dict) and 'message' in response:
                    message_obj = response['message']
                    if isinstance(message_obj, dict) and 'content' in message_obj:
                        content_list = message_obj['content']
                        if isinstance(content_list, list) and len(content_list) > 0:
                            text_content = content_list[0]
                            if isinstance(text_content, dict) and 'text' in text_content:
                                response_text = text_content['text']
                            else:
                                response_text = str(content_list[0])
                        else:
                            response_text = str(response)
                    else:
                        response_text = str(response)
                else:
                    response_text = str(response)
            except Exception as parse_error:
                logger.warning(f"Could not parse response: {parse_error}")
                response_text = str(response)
            
            # Send the response
            yield f"data: {json.dumps({'type': 'response', 'content': response_text})}\n\n"
            
            # Send end event
            yield f"data: {json.dumps({'type': 'end', 'success': True})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in stream: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/tools")
async def get_tools():
    """
    Get list of available tools
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    tools_info = []
    for tool in tools_list[:30]:  # Limit to first 30 for display
        try:
            tool_name = getattr(tool, 'tool_name', 'Unknown')
            tool_desc = getattr(tool, 'description', 'No description')
            tools_info.append({
                "name": tool_name,
                "description": tool_desc
            })
        except Exception as e:
            logger.warning(f"Could not get tool info: {str(e)}")
    
    return {
        "total_tools": len(tools_list),
        "tools": tools_info,
        "mcp_connected": mcp_connected
    }

@app.get("/api/status")
async def get_status():
    """
    Get agent status
    """
    if agent is None:
        return AgentStatus(
            status="initializing",
            tools_count=0,
            model="qwen2.5:1.5b",
            mcp_connected=False
        )
    
    return AgentStatus(
        status="ready",
        tools_count=len(tools_list),
        model="qwen2.5:1.5b",
        mcp_connected=mcp_connected
    )

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "agent_ready": agent is not None,
        "tools_available": len(tools_list)
    }

# ========================
# Error handlers
# ========================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {"error": str(exc)}

# ========================
# Main
# ========================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 DevOps AI Agent API")
    print("="*60)
    print("🌐 Starting server on http://localhost:3000")
    print("📝 API docs: http://localhost:3000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        log_level="info"
    )
