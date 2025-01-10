from redis_om import EmbeddedJsonModel, JsonModel, Migrator


class ImageUrl(EmbeddedJsonModel):
    url: str = None

class Content(EmbeddedJsonModel):
    type: str
    text: str = None
    image_url: ImageUrl = None

class Message(EmbeddedJsonModel):
    role: str
    content: str | list[Content]

class ChatSession(JsonModel):
    messages: list[Message] = []
    totallyTokenUsage: int = 0
    
    # override save() to set expire time
    def save(self):
        self.expire(3600)

        return super().save()


Migrator().run()
