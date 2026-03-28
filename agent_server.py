from strands import Agent
from openai import OpenAI

# connect to Ollama (local)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# create agent
agent = Agent(
    model="qwen2.5:1.5b",
    client=client
)

# add tools
from tools import run_shell, get_time, disk_usage, kubectl_get_pods, get_weather

agent.add_tool(run_shell)
agent.add_tool(get_time)
agent.add_tool(disk_usage)
agent.add_tool(kubectl_get_pods)

# run loop
while True:
    user_input = input("\nAsk DevOps AI > ")
    response = agent(user_input)
    print("\n🤖:", response)