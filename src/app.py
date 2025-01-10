# set environment
# import setting.Env

# import tiktoken

from infra.Fastapi import app
from infra.Response import CustomResponse, ResponseStruct
from handler.RequestHandler import create_session_handler, chat_handler, chat_history_handler


'''
Get parameter in request
    query -> define functional variable's type to "str". ex. def function(var:str)
    path -> don't define any type, and add the variable into url with {}. ex. @app.get(/path/{var})
    request body -> define to "dict", "list". ex. def function(var:dict)
'''

@app.get("/session/create")
def create_session():
    result = create_session_handler()

    return CustomResponse(ResponseStruct(result=result))

@app.post("/chat/{sessionID}")
def chat_with_gpt(sessionID, eventData:dict):
    prompt = eventData["prompt"]
    result = chat_handler(sessionID, prompt)

    return CustomResponse(ResponseStruct(result=result))

@app.get("/history/{sessionID}")
def get_chat_history(sessionID):
    result = chat_history_handler(sessionID)

    return CustomResponse(ResponseStruct(result=result))