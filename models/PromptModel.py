
class PromptRole:
    system:str = "system"
    user:str = "user"
    assistant:str = "assistant"

class PromptMessage():
    def prompt_format( self, role: str, content:str ) -> dict:
        return { "role": role, "content": content }

class SystemPrompt( PromptMessage ):
    def prompt_format(self, content:str) -> dict:
        return { "role": PromptRole.system, "content": content }

class UserPrompt( PromptMessage ):
    def prompt_format(self, content:str) -> dict:
        return { "role": PromptRole.user, "content": content }

class AssistantPrompt( PromptMessage ):
    def prompt_format(self, content:str) -> dict:
        return { "role": PromptRole.assistant, "content": content }

class PromptMessageList():
    def __init__(self):
        self.init_messages()

    def init_messages(self):
        self.messages = []
    
    def set_system_prompt(self, content: str):
        self.init_messages()
        system_prompt = SystemPrompt().prompt_format(content)
        self.messages = [system_prompt]

    def add_user_input(self, content: str):
        user_prompt = UserPrompt().prompt_format(content)
        self.messages.append(user_prompt)

    def add_assistant_output(self, content: str):
        assistant_prompt = AssistantPrompt().prompt_format(content)
        self.messages.append(assistant_prompt)

    def get_messages(self) -> list:
        return self.messages
    
    def get_system_prompt(self) -> str|None:
        return self.messages[0]["content"] if self.messages else None