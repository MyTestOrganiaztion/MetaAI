
from models.PromptModel import PromptRole
from models.RedisDataStructure import ImageUrl, Content, Message, ChatSession


class Transformer:

    @staticmethod
    def from_redis_message_to_dict(redisMessage:Message) -> dict[str, str|list[dict]]:
        messageDump:dict[str, str|list[Content]] = {"role": redisMessage.role, "content": redisMessage.content}
        if isinstance(messageDump["content"], list):
            for _id, content in enumerate(messageDump["content"]):
                if content.type == "text":
                    messageDump["content"][_id] = {"type": content.type, content.type: content.text}

                elif content.type == "image_url":
                    messageDump["content"][_id] = {"type": content.type, content.type: content.image_url.model_dump(exclude="pk", exclude_unset=True)}
                    
        return messageDump

    @staticmethod
    def from_dict_to_redis_message(role:str, _content:str|dict) -> Message:
        if isinstance(_content, dict):
            if _content["type"] == "image_url":
                _content[_content["type"]] = ImageUrl(**{"url": _content[_content["type"]]["url"]})
            
            content = Content(**{"type": _content["type"], _content["type"]: _content[_content["type"]]})

            return Message(**{"role": role, "content": [content]})
        return Message(**{"role": role, "content": _content})


class ChatSessionController():
    def __init__(self, sessionID:str):
        self.sessionID = sessionID
        self.session = ChatSession.get(sessionID)

    def update_token_usage(self, promptTokenUsage:int, completionTokenUsage:int) -> None:
        self.session.totallyTokenUsage += promptTokenUsage + completionTokenUsage
        self.session.save()

    def get_token_usage(self) -> int:
        return self.session.totallyTokenUsage

    def add_message(self, promptMessage:Message) -> None:
        if promptMessage.role == PromptRole.USER and self.session.messages[-1].role == PromptRole.USER:
            self.session.messages[-1].content.extend(promptMessage.content)
        
        else:
            self.session.messages.append(promptMessage)
        
        self.session.save()

    def set_system_prompt(self, content:str) -> None:
        promptMessage = Transformer.from_dict_to_redis_message(PromptRole.SYSTEM, content)
        self.add_message(promptMessage)
    
    def add_user_message(self, content:dict, isImage:bool=False) -> None:
        if isImage:
            promptMessage = Transformer.from_dict_to_redis_message(PromptRole.USER, {"type": "image_url", "image_url": {"url": content}})
        
        else:
            promptMessage = Transformer.from_dict_to_redis_message(PromptRole.USER, {"type": "text", "text":content})
        
        self.add_message(promptMessage)

    def add_assistant_message(self, content:str, promptTokenUsage:int=0, completionTokenUsage:int=0) -> None:
        promptMessage = Transformer.from_dict_to_redis_message(PromptRole.ASSISTANT, content)
        self.add_message(promptMessage)
        self.update_token_usage(promptTokenUsage, completionTokenUsage)

    def get_messages(self) -> list[dict]:
        
        return [Transformer.from_redis_message_to_dict(message.model_copy(deep=True)) for message in self.session.messages]
    
    @staticmethod
    def is_session_exists(sessionID:str) -> bool:
        return True if ChatSession.get(sessionID) else False

    @staticmethod
    def create_session() -> str:
        '''Generate session, return session ID'''
        session = ChatSession(**{"messages": []}).save()

        return session.pk