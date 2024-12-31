
from models.PromptModel import PromptMessageList
from reference.chatGPT import chat_completions_create
from .ResponseHandler import error_handler
from ..helper.PromptParser import extract_urls, get_website_content, replace_urls_with_text

from openai.types.chat import ChatCompletion
from fastapi import Response

promptMessages = PromptMessageList()

# @error_handler
# def set_prompt_handler(response:Response, eventData:dict=None):
#     prompt = eventData["prompt"]
#     promptMessages.init_messages(prompt)
#     return {"prompt": promptMessages.get_system_prompt()}

@error_handler
def chat_handler(response:Response, eventData:dict=None):
    prompt = eventData["prompt"]
    urls = extract_urls(prompt)
    for url in urls:
        websiteContent, imgUrls = get_website_content(url)
        prompt = replace_urls_with_text(prompt, url, websiteContent)
        for imgUrl in imgUrls:
            promptMessages.add_user_input(imgUrl, isImage=True)
    
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
def get_chat_history_handler(response:Response, eventData:dict=None):
    return promptMessages.get_messages()