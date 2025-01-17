from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infra.Response import CustomResponse
from handler.ExceptionHandler import add_handler


_app = FastAPI(default_response_class=CustomResponse)
_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = add_handler(_app)