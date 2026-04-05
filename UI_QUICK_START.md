# FastAPI + HTML UI - Quick Start Guide

Your DevOps AI Agent now has a **professional web interface** built with FastAPI and custom HTML/CSS!

## 📦 What You Get

- **Backend**: FastAPI REST API (`app.py`)
- **Frontend**: Beautiful responsive HTML UI (`index.html`)
- **No Node.js needed**: Pure Python + vanilla JavaScript
- **Production-ready**: Proper error handling and streaming support

---

## 🚀 Quick Start

### Step 1: Install FastAPI (if not already installed)

```bash
pip install fastapi uvicorn
```

Or install from requirements:
```bash
pip install -r requirement.txt
```

### Step 2: Start the Server

```bash
python app.py
```

You should see:
```
============================================================
🚀 DevOps AI Agent API
============================================================
🌐 Starting server on http://localhost:8000
📝 API docs: http://localhost:8000/docs
============================================================
```

### Step 3: Open in Browser

Navigate to:
```
http://localhost:8000
```

**That's it!** Your AI agent is now accessible via a beautiful web interface! 🎉

---

## 🎨 UI Features

### Left Sidebar
- **Status Indicator**: Shows if agent is ready (green = ready, red = offline)
- **Tools List**: Grouped by category (Kubernetes, Custom, System)
- **Tool Count**: Total number of available tools

### Main Chat Area
- **Clean Chat Interface**: User messages on right, AI responses on left
- **Loading Animation**: Shows when agent is processing
- **Auto-scroll**: Automatically scrolls to latest message
- **Empty State**: Helpful message when first opened

### Input Area
- **Auto-expanding textarea**: Grows as you type (max 120px)
- **Keyboard shortcuts**: 
  - `Ctrl+Enter` - Send message
  - `Enter` alone - New line
- **Send Button**: Send your message to the agent
- **Clear Button**: Clear all chat history

---

## 📡 API Endpoints

All endpoints are REST APIs you can call directly:

### Chat

**Send a message:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "List all pods", "conversation_history": []}'
```

**Response:**
```json
{
  "success": true,
  "response": "Pods in default namespace:\n- pod1 (Running)\n- pod2 (Pending)",
  "message": "List all pods"
}
```

### Tools

**Get available tools:**
```bash
curl "http://localhost:8000/api/tools"
```

**Response:**
```json
{
  "total_tools": 37,
  "tools": [
    {"name": "list_pods", "description": "List all pods in a Kubernetes namespace"},
    {"name": "add_numbers", "description": "Add two numbers together"},
    ...
  ],
  "mcp_connected": true
}
```

### Status

**Check agent status:**
```bash
curl "http://localhost:8000/api/status"
```

**Response:**
```json
{
  "status": "ready",
  "tools_count": 37,
  "model": "qwen2.5:1.5b",
  "mcp_connected": true
}
```

### Health

**Health check:**
```bash
curl "http://localhost:8000/api/health"
```

---

## 📋 Example Queries to Try

### Kubernetes Operations
```
List all pods in the default namespace
Show me the deployment details for nginx
Get resource usage for pods
List all services in kube-system namespace
Get cluster information
```

### Calculations
```
What is 15 plus 25?
Add 100 and 200
```

### System Info
```
What is the current time?
Check disk usage
Generate a random number
```

### Combined Operations
```
Get the number of pods and add 10 to that number
List deployments in default namespace and show me their details
```

---

## 🔧 Configuration

### Change Port

Edit `app.py` and find:
```python
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,  # Change this
        log_level="info"
    )
```

### Change Host

To only listen on localhost:
```python
host="127.0.0.1",  # Instead of "0.0.0.0"
```

### Logging Level

Change log level:
```python
log_level="debug"  # Options: critical, error, warning, info, debug, trace
```

---

## 🐛 Troubleshooting

### Port 8000 Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port in app.py
```

### Agent Not Responding

1. **Check Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Check FastMCP is running (if using custom tools):**
   ```bash
   curl http://localhost:8000/sse
   ```

3. **Check agent initialization in logs:**
   - Look for "✅ Agent initialized" message
   - Check for any error messages

### Tools Not Showing

1. Check `api/tools` endpoint:
   ```bash
   curl http://localhost:8000/api/tools
   ```

2. Verify tools are defined in code:
   - Check `tools.py`
   - Check `kubernetes_tools.py`
   - Check imports in `app.py`

### UI Not Loading

1. Verify `index.html` exists in same directory as `app.py`
2. Check browser console for errors (F12)
3. Verify server is running (should see "Starting server on..." message)

---

## 📊 File Structure

```
Devops_with_ai/
├── app.py                    # FastAPI backend
├── index.html               # Web UI
├── tools.py                 # System tools
├── kubernetes_tools.py      # K8s tools
├── tools_pdf.py            # PDF tools
└── requirement.txt         # Dependencies
```

---

## 🚀 Production Deployment

For production deployments, consider:

1. **Using a process manager:**
   ```bash
   pip install gunicorn
   gunicorn app:app -w 4 -b 0.0.0.0:8000
   ```

2. **Using systemd service:**
   ```ini
   [Unit]
   Description=DevOps AI Agent
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/project
   ExecStart=/path/to/venv/bin/python app.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Using Docker:**
   ```dockerfile
   FROM python:3.14
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "app.py"]
   ```

4. **Using a reverse proxy (nginx):**
   ```nginx
   location / {
       proxy_pass http://localhost:8000;
       proxy_set_header Host $host;
   }
   ```

---

## 📚 Next Steps

1. ✅ Start the server: `python app.py`
2. ✅ Open browser: `http://localhost:8000`
3. ✅ Try some queries
4. ✅ Customize as needed

---

## 🎁 Tips

- **Custom Styling**: Edit CSS in `index.html` between `<style>` tags
- **Add Features**: Modify JavaScript in `<script>` section
- **New Tools**: Add them to `kubernetes_tools.py` or `tools.py`, then restart
- **API Integration**: Use the REST endpoints to integrate with other apps

---

## 📞 Need Help?

Check the relevant documentation:
- FastAPI docs: http://localhost:8000/docs
- Agent functionality: See README.md
- Kubernetes tools: See kubernetes_tools.py comments
- System tools: See tools.py comments

Enjoy your new AI-powered DevOps agent! 🚀
