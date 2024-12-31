# import tiktoken
# from typing import Union
from fastapi import FastAPI, Response

from handler.RequestHandler import *

app = FastAPI()

'''
Get parameter in request
    query -> define functional variable's type to "str". ex. def function(var:str)
    path -> don't define any type, and add the variable into url with {}. ex. @app.get(/path/{var})
    request body -> define to "dict", "list". ex. def function(var:dict)
'''

@app.post("/setprompt")
def set_prompt(response:Response, eventData:dict):
    result = set_prompt_handler(response, eventData)

    return result

@app.post("/chat")
def chat_without_prompt(response:Response, eventData:dict):
    result = chat_handler(response, eventData)

    return result

@app.get("/chathistory")
def get_chat_history(response:Response):
    result = get_chat_history_handler(response)

    return result