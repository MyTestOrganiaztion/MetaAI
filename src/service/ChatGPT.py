from openai import OpenAI
import os


GPT_API_KEY = os.getenv("GPT_API_KEY")
MODEL = "gpt-4-turbo-2024-04-09"
client = OpenAI( api_key=GPT_API_KEY )

def chat_completions_create(messages:list[dict]) -> None:
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
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