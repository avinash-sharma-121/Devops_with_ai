from strands import Agent, tool
from strands_tools import calculator, http_request
from strands.models.ollama import OllamaModel

# add tools
from tools import about_me, run_shell, get_time, disk_usage, kubectl_get_pods,get_weather,random_number

from tools_pdf import read_pdf,generate_pdf

#define loacl model
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen2.5:1.5b"
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

agent= Agent(
    model=ollama_model,
    tools=[calculator, http_request,about_me,read_pdf, generate_pdf, random_number, run_shell,get_time,disk_usage,kubectl_get_pods,get_weather],
    system_prompt=system_prompt
    )

# By default, it run Amazon Bedrock, but you can specify any other model by passing the model name as an argument to the Agent constructor.
# For example, to use Anthropic Claude 2, you can do:
# agent = Agent(model="anthropic.claude-2")




user_input=input("What do you want to ask the agent? ")

agent(user_input)
