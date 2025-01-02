
class SystemPromptPattern:
    BASIC = '''
        你是一名專業的廣告顧問。你的任務是根據使用者提供的輸入（可能是幾個關鍵字或一個網頁內容）進行分析，並回答以下問題：
        1.該內容或網站的目標受眾是哪些群體（例如：年齡、性別、興趣等）。
        2.為該目標受眾撰寫一條吸引他們的廣告文案，需強調獨特價值並激發行動力，字數限制100個字。
        請以日文清晰且具體地回答，以便提供實用的建議。
    '''
    TEXT_ONLY:str = "根據使用者輸入的文字描述，提供建議的廣告受眾並撰寫廣告文案。"
    WEB_LINK_ONLY:str = "根據使用者輸入的網頁內容，提供建議的廣告受眾並撰寫廣告文案。"
    TEXT_AND_WEB:str = "根據使用者輸入的關鍵字以及網頁內容，分析合適的廣告受眾，並撰寫一條廣告文案"
    IMAGE_URL_ONLY:str = "What’s in this image and what kind of person will be interested in it?"
    
class PromptRole:
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class PromptMessage:
    def __init__(self, role:str, content:str|list = None):
        self.role = role
        self.content = content

    def add_content(self, contentItem:str|dict):
        """Adds content to the message."""
        self.content.append(contentItem)

    def to_dict(self) -> dict:
        """Converts the message to a dictionary format."""
        return {"role": self.role, "content": self.content}

class PromptMessageList:
    def __init__(self):
        # Initialize with a default system message
        self.messages = [PromptMessage(PromptRole.SYSTEM, SystemPromptPattern.BASIC)]

    def add_message(self, role: str, contentItem: str | dict):
        """Adds a new message or updates an existing one based on the role."""
        if role == PromptRole.SYSTEM and self.messages[0].role == PromptRole.SYSTEM:
            self.messages[0].content += f"\n{contentItem}"  # Append to existing system content
        
        elif role == PromptRole.USER and self.messages[-1].role == PromptRole.USER:
            self.messages[-1].add_content(contentItem)  # Append to existing user content
        
        elif role == PromptRole.ASSISTANT:
            self.messages.append(PromptMessage(role, contentItem))
        
        else:
            self.messages.append(PromptMessage(role, [contentItem]))

    def set_system_prompt(self, content: str):
        """Sets the system prompt."""
        self.add_message(PromptRole.SYSTEM, content)

    def add_user_message(self, content: dict, isImage:bool=False):
        """Adds a user message."""
        if isImage:
            self.add_message(PromptRole.USER, {"type": "image_url", "image_url": {"url": content}})
        
        else:
            self.add_message(PromptRole.USER, {"type": "text", "text":content})

    def add_assistant_message(self, content: str):
        """Adds an assistant message."""
        self.add_message(PromptRole.ASSISTANT, content)

    def get_messages(self) -> list:
        """Returns all messages in dictionary format."""
        
        return [message.to_dict() for message in self.messages]

    def get_system_prompt(self) -> str | None:
        """Returns the concatenated system prompt."""
        
        return " ".join(self.messages[0].content) if self.messages and self.messages[0].role == PromptRole.SYSTEM else None
