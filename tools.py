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

@tool
def random_number() -> str:
    """Generate a random number between 1 and 100"""
    import random
    return str(random.randint(1, 100))

@tool
def generate_pdf(content: str) -> str:
    """Generate a PDF file from the given content"""
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output("output.pdf")
    return "PDF generated successfully as output.pdf"

#@tool
#def read_file(file_path: str) -> str:
#    """Read the content of a file"""
#    try:
#        with open(file_path, 'r') as file:
#            return file.read()
#    except Exception as e:
#        return str(e)


@tool
def about_me() -> str:
    """Return information about the developer and the agent"""
    return "I am a helpful assistant built using Strands framework. I can perform various tasks using the tools provided to me."

