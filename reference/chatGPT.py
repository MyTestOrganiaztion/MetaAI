from openai import OpenAI

from env import API_KEY

from models.PromptModel import PromptMessageList


MODEL = "gpt-4o"
client = OpenAI( api_key=API_KEY )

def chat_completions_create(messages:PromptMessageList):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages.get_messages()
    )
