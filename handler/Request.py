
from models.PromptModel import PromptMessageList
from reference.chatGPT import chat_completions_create
from .Response import error_handler

from openai.types.chat import ChatCompletion

promptMessages = PromptMessageList()

@error_handler
def set_prompt_handler(event:dict, context:None=None):
    prompt = event["prompt"]
    promptMessages.set_system_prompt(prompt)
    return {"prompt": promptMessages.get_system_prompt()}

@error_handler
def chat_without_prompt_handler(event:dict, context:None=None):
    prompt = event["prompt"]
    promptMessages.add_user_input(prompt)
    completion:ChatCompletion = chat_completions_create(promptMessages)
    promptMessages.add_assistant_output(completion.choices[0].message.content)
    tokenUsage = completion.usage
    promptTokenUsage = tokenUsage.prompt_tokens
    completionTokenUsage = tokenUsage.completion_tokens
    return {
      "prompt": prompt, 
      "completion": completion.choices[0].message.content, 
      "prompt token usage": promptTokenUsage,
      "completion token usage": completionTokenUsage,
      "total token usage": promptTokenUsage + completionTokenUsage
    }

@error_handler
def get_chat_history_handler(event:dict=None, context:None=None):
    return promptMessages.get_messages()