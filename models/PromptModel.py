
class SystemPromptPattern():
    pureText:str = "Create a advertising copy from some keywords."
    pureWebsiteUrl:str = ""
    TextAndWebsite:str = ""
    pureImageUrl:str = "What’s in this image and what kind of person will be interested in it?"

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

class UserPromptImage( PromptMessage ):
    def prompt_format(self, content:str) -> dict:
        return { "role": PromptRole.user, "content": [{"type": "image_url", "image_url": {"url": content}}] }

class AssistantPrompt( PromptMessage ):
    def prompt_format(self, content:str) -> dict:
        return { "role": PromptRole.assistant, "content": content }

class PromptMessageList():
    def __init__(self):
        system_prompt = SystemPrompt().prompt_format("You're a Japaneses advertisement adviser.")
        self.messages = [system_prompt]
    
    def add_system_prompt(self, content: str):
        system_prompt = SystemPrompt().prompt_format(content)
        self.messages.append(system_prompt)

    def add_user_input(self, content: str, isImage:bool=False):
        if isImage:
            user_prompt = UserPromptImage().prompt_format(content)

        else:
            user_prompt = UserPrompt().prompt_format(content)
    
        self.messages.append(user_prompt)

    def add_assistant_output(self, content: str):
        assistant_prompt = AssistantPrompt().prompt_format(content)
        self.messages.append(assistant_prompt)

    def get_messages(self) -> list:
        return self.messages
    
    def get_system_prompt(self) -> str|None:
        return self.messages[0]["content"] if self.messages else None