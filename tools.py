from strands import tool
import subprocess
from datetime import datetime

@tool
def run_shell(command: str) -> str:
    """Run a shell command"""
    try:
        return subprocess.check_output(command, shell=True, text=True)
    except Exception as e:
        return str(e)

@tool
def get_time() -> str:
    """Get current system time"""
    return str(datetime.now())

@tool
def disk_usage() -> str:
    """Check disk usage"""
    return subprocess.getoutput("df -h")

@tool
def kubectl_get_pods() -> str:
    """Get Kubernetes pods"""
    return subprocess.getoutput("kubectl get pods -n kube-system")

@tool

def get_weather(city: str) -> str:
    """Get current weather for a city using wttr.in"""
    import requests
    try:
        response = requests.get(f"http://wttr.in/{city}?format=3")
        if response.status_code == 200:
            return response.text
        else:
            return f"Error fetching weather: {response.status_code}"
    except Exception as e:
        return str(e)