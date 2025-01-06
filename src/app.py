# import tiktoken

from infra.Fastapi import app
from infra.Response import CustomResponse, ResponseStruct
from handler.RequestHandler import *


'''
Get parameter in request
    query -> define functional variable's type to "str". ex. def function(var:str)
    path -> don't define any type, and add the variable into url with {}. ex. @app.get(/path/{var})
    request body -> define to "dict", "list". ex. def function(var:dict)
'''


@app.post("/chat")
def chat_with_gpt(eventData:dict):
    prompt = eventData["prompt"]
    result = chat_handler(prompt)

    return CustomResponse(ResponseStruct(result=result))

@app.get("/history")
def get_chat_history():
    result = chat_history_handler()

    return CustomResponse(ResponseStruct(result=result))