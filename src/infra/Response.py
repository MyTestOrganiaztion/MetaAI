from fastapi.responses import JSONResponse
from pydantic import BaseModel

from typing import Any


class ResponseStruct(BaseModel):
    code:str = "OK000"
    detail:str = ""
    result:Any

class CustomResponse(JSONResponse):
    def __init__(self, response:ResponseStruct, status_code:int=200, *args, **kwargs):
        content = response.model_dump()
        super().__init__(content=content, status_code=status_code, *args, **kwargs)
