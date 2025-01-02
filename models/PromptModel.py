
class SystemPromptPattern:
    BASIC = '''
        あなたはプロの広告コンサルタントです。ユーザーから提供された情報（キーワードやウェブサイトの内容など）を基に分析を行い、以下の質問に答えてください：
        1.この内容またはウェブサイトのターゲットとなるユーザー層はどのような人々ですか？（例：年齢、性別、興味、行動特性など）
        2.そのターゲット層を引き付ける広告文を作成してください。広告文は独自の価値を強調し、行動を促すものであり、100文字以内に収めてください。
        回答は日本語で明確かつ具体的に行い、実用的な提案を提供してください。
    '''
    TEXT_ONLY:str = "ユーザーが提供したテキストの説明を基に、適切な広告ターゲット層（例：年齢、性別、興味など）を分析し、そのターゲット層を引き付ける広告文を作成してください。広告文は、独自の価値を強調し、行動を促すものであり、100文字以内に収めてください。回答は必ず日本語で記載してください。"
    WEB_LINK_ONLY:str = "ユーザーが提供したウェブサイトの内容を基に、適切な広告ターゲット層（例：年齢、性別、興味など）を分析し、そのターゲット層に向けた広告文を作成してください。広告文は、サイトの独自の価値を強調し、行動を促す内容とし、100文字以内にしてください。回答は必ず日本語で記載してください。"
    TEXT_AND_WEB:str = "ユーザーが提供したキーワードとウェブサイトの内容を総合的に分析し、適切な広告ターゲット層（例：年齢、性別、興味など）を特定してください。その上で、ターゲット層を引き付ける広告文を作成してください。広告文は、独自の価値を強調し、行動を促す内容とし、100文字以内にしてください。回答は必ず日本語で記載してください。"
    IMAGE_URL_ONLY:str = "提供された画像の内容を基に、その画像が伝えるメッセージを分析し、関心を持つ可能性が高いターゲット層（例：年齢、性別、興味など）を特定してください。そのターゲット層に向けて広告文を作成してください。広告文は、画像の魅力や価値を強調し、行動を促す内容とし、100文字以内にしてください。回答は必ず日本語で記載してください。"
    
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
