from fastapi import FastAPI

from infra.Response import CustomResponse
from handler.ExceptionHandler import add_handler


_app = FastAPI(default_response_class=CustomResponse)

app = add_handler(_app)