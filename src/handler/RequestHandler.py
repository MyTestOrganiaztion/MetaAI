
from models.PromptModel import SystemPromptPattern
from service.ChatGPT import chat_completions_create
from helper.WebParser import extract_urls, get_website_content, replace_urls_with_text
from service.RedisCRUD import ChatSessionController

from openai.types.chat import ChatCompletion


def create_session_handler() -> str:
    chatSessionID = ChatSessionController.create_session()
    
    return {"sessionID": chatSessionID}

def chat_handler(chatSessionID:str, prompt:str) -> dict:
    chatController = ChatSessionController(chatSessionID)
    urls, nonUrls = extract_urls(prompt)

    if not chatController.get_messages():
        if urls and nonUrls:
            chatController.set_system_prompt(SystemPromptPattern.BASIC.format(SystemPromptPattern.TEXT_AND_WEB))
        elif urls:
            chatController.set_system_prompt(SystemPromptPattern.BASIC.format(SystemPromptPattern.WEB_LINK_ONLY))
        else:
            chatController.set_system_prompt(SystemPromptPattern.BASIC.format(SystemPromptPattern.TEXT_ONLY))

    for url in urls:
        websiteContent, imgUrls = get_website_content(url)
        prompt = replace_urls_with_text(prompt, url, websiteContent)
        for imgUrl in imgUrls:
            chatController.add_user_message(imgUrl, isImage=True)
        # promptMessages.add_user_message(url, isImage=True)
    
    chatController.add_user_message(prompt)
    promptMessages = chatController.get_messages()
    completion:ChatCompletion = chat_completions_create(promptMessages)
    tokenUsage = completion.usage
    promptTokenUsage = tokenUsage.prompt_tokens
    completionTokenUsage = tokenUsage.completion_tokens
    chatController.add_assistant_message(completion.choices[0].message.content, (promptTokenUsage+completionTokenUsage))
    
    return {
      "prompt": prompt, 
      "completion": completion.choices[0].message.content, 
      "promptTokenUsage": promptTokenUsage,
      "completionTokenUsage": completionTokenUsage,
      "totalTokenUsage": promptTokenUsage + completionTokenUsage
    }

def chat_history_handler(chatSessionID:str) -> list:
    chatController = ChatSessionController(chatSessionID)
    
    return chatController.get_messages()