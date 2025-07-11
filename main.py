import getpass
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage

model = init_chat_model("gpt-3.5-turbo", model_provider="openai")
response = model.invoke([
        HumanMessage(content="Hi! I'm Bob"),
        AIMessage(content="Hello Bob! How can I assist you today?"),
        HumanMessage(content="What's my name?"),
    ])
print(response)