from strands import Agent, tool
from strands_tools import calculator, http_request
from strands.models.ollama import OllamaModel

# add tools
from tools import run_shell, get_time, disk_usage, kubectl_get_pods,get_weather


#define loacl model
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen2.5:1.5b"
)

system_prompt = "You are a helpful assistant."\
      "you give answers in a kind and informative manner."\
        "you can use correct data sources to answer the user's question."\
          "you can use the tools and free apis to get the correct answer for the user."\
            "if you don't know the answer, you can say you don't know instead of making up an answer."

agent= Agent(
    model=ollama_model,
    tools=[calculator, http_request, run_shell,get_time,disk_usage,kubectl_get_pods,get_weather],
    system_prompt=system_prompt
    )

# By default, it run Amazon Bedrock, but you can specify any other model by passing the model name as an argument to the Agent constructor.
# For example, to use Anthropic Claude 2, you can do:
# agent = Agent(model="anthropic.claude-2")




user_input=input("What do you want to ask the agent? ")

agent(user_input)
