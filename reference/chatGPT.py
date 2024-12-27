from dotenv import load_dotenv
import os
from openai import OpenAI
from openai import APIConnectionError

from models.PromptModel import PromptMessageList


load_dotenv()

API_KEY = os.getenv("GPT_API_KEY")

MODEL = "gpt-4o"
client = OpenAI( api_key=API_KEY )

def chat_completions_create(messages:PromptMessageList):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages.get_messages()
    )
