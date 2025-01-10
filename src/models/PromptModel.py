
class SystemPromptPattern:
    BASIC = '''
        你是一個日本的廣告行銷專家，你的回答內容必須聚焦於廣告文案與目標受眾分析，對於其他類型的問題（如技術編碼或非廣告相關的內容），請直接回應『この様なの問題はお答えできません。』，並且一切對答必須使用日文。
        {}請告訴我容易對所提供的內容感興趣的受眾的"年齡分布"、"興趣"、"性別"，並根據你推測的受眾去撰寫一篇日文廣告文案，確保文案能促進受眾的慾望及好奇心。
    '''
    TEXT_ONLY:str = '''
        根據我提供的描述或關鍵字，
    '''
    WEB_LINK_ONLY:str = '''
        根據我提供的網頁文字內容以及其中包含的圖片，
    '''
    TEXT_AND_WEB:str = '''
        根據我的網頁內容和和提示，
    '''
    IMAGE_URL_ONLY:str = '''
        根據我提供的圖像連結，
    '''
    
class PromptRole:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

# class PromptMessage:
#     def __init__(self, role:str, content:str|list="", promptTokenUsage:int=0, completionTokenUsage:int=0):
#         self.role = role
#         self.content = content

#     def add_content(self, contentItem:str|dict):
#         """Adds content to the message."""
#         self.content.append(contentItem)

#     def to_dict(self) -> dict:
#         """Converts the message to a dictionary format."""
#         return {"role": self.role, "content": self.content}

# class PromptMessageList:
#     def __init__(self):
#         # Initialize with a default system message
#         self.messages = [PromptMessage(PromptRole.SYSTEM, SystemPromptPattern.BASIC)]

#     def add_message(self, role: str, contentItem: str | dict):
#         """Adds a new message or updates an existing one based on the role."""
#         if role == PromptRole.SYSTEM and self.messages[0].role == PromptRole.SYSTEM:
#             self.messages[0].content = SystemPromptPattern.BASIC.format(contentItem)  # Append to existing system content
        
#         elif role == PromptRole.USER and self.messages[-1].role == PromptRole.USER:
#             self.messages[-1].add_content(contentItem)  # Append to existing user content
        
#         elif role == PromptRole.ASSISTANT:
#             self.messages.append(PromptMessage(role, contentItem))
        
#         else:
#             self.messages.append(PromptMessage(role, [contentItem]))

#     def set_system_prompt(self, content:str):
#         """Sets the system prompt."""
#         self.add_message(PromptRole.SYSTEM, content)

#     def add_user_message(self, content:dict, isImage:bool=False):
#         """Adds a user message."""
#         if isImage:
#             self.add_message(PromptRole.USER, {"type": "image_url", "image_url": {"url": content}})
        
#         else:
#             self.add_message(PromptRole.USER, {"type": "text", "text":content})

#     def add_assistant_message(self, content: str):
#         """Adds an assistant message."""
#         self.add_message(PromptRole.ASSISTANT, content)

#     def get_messages(self) -> list:
#         """Returns all messages in dictionary format."""
        
#         return [message.to_dict() for message in self.messages]

#     def get_system_prompt(self) -> str | None:
#         """Returns the concatenated system prompt."""
        
#         return " ".join(self.messages[0].content) if self.messages and self.messages[0].role == PromptRole.SYSTEM else None
