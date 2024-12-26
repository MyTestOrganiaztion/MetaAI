import tiktoken
from typing import Union
from fastapi import FastAPI

from handler.Request import *

app = FastAPI()

'''
Get parameter in request
    query -> define functional variable's type to "str". ex. def function(var:str)
    path -> don't define any type, and add the variable into url with {}. ex. @app.get(/path/{var})
    request body -> define to "dict", "list". ex. def function(var:dict)
'''

@app.post("/setprompt")
def set_prompt(eventData: dict):
    result = set_prompt_handler(eventData)

    return result

@app.post("/chat")
def chat_without_prompt(eventData: dict):
    result = chat_without_prompt_handler(eventData)

    return result

@app.get("/chathistory")
def get_chat_history():
    result = get_chat_history_handler()

    return result