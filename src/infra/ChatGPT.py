from openai import OpenAI

from infra.env import GPT_API_KEY

from models.PromptModel import PromptMessageList


MODEL = "gpt-4-turbo-2024-04-09"
client = OpenAI( api_key=GPT_API_KEY )

def chat_completions_create(messages:PromptMessageList):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages.get_messages(),
        temperature=0.7
    )

# list up models
def list_models():
    models = client.models.list()
    for model in models:
        print(model)
        with open("gpt_models.txt", "a") as f:
            f.write(model.to_json() + ",\n")


if __name__ == "__main__":
    list_models()