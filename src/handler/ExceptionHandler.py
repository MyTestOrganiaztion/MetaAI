
from infra.Response import ResponseStruct, CustomResponse

from typing import Callable
from fastapi import Request
from openai import RateLimitError, APIConnectionError, APITimeoutError, AuthenticationError, PermissionDeniedError
from requests.exceptions import ConnectionError
from redis_om.model.model import NotFoundError
from fastapi import FastAPI, status


def create_exception_handler(statusCode:int, errorCode:str, result:str) -> Callable[[Request, Exception], CustomResponse]:
    response = ResponseStruct(
        code=errorCode,
        detail="",
        result=result
    )
    async def exception_handler(request:Request, exception:Exception):
        response.detail = exception.__str__()

        return CustomResponse(response=response, status_code=statusCode)
    
    return exception_handler

def add_handler(_app:FastAPI) -> FastAPI:
    
    _app.add_exception_handler(
        RateLimitError,
        create_exception_handler(
            statusCode=RateLimitError.status_code,
            errorCode="ER000",
            result="RateLimitError"
        )
    )

    _app.add_exception_handler(
        APIConnectionError,
        create_exception_handler(
            statusCode=status.HTTP_503_SERVICE_UNAVAILABLE,
            errorCode="ER001",
            result="APIConnectionError"
        )
    )


    _app.add_exception_handler(
        APITimeoutError,
        create_exception_handler(
            statusCode=status.HTTP_408_REQUEST_TIMEOUT,
            errorCode="ER002",
            result="APITimeoutError"
        )
    )

    _app.add_exception_handler(
        AuthenticationError,
        create_exception_handler(
            statusCode=AuthenticationError.status_code,
            errorCode="ER003",
            result="AuthenticationError"
        )
    )

    _app.add_exception_handler(
        PermissionDeniedError,
        create_exception_handler(
            statusCode=PermissionDeniedError.status_code,
            errorCode="ER004",
            result="PermissionDeniedError"
        )
    )

    _app.add_exception_handler(
        KeyError,
        create_exception_handler(
            statusCode=status.HTTP_400_BAD_REQUEST,
            errorCode="ER005",
            result="KeyError"
        )
    )

    _app.add_exception_handler(
        ConnectionError,
        create_exception_handler(
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errorCode="SYS000",
            result="ConnectionError"
        )
    )

    _app.add_exception_handler(
        NotFoundError,
        create_exception_handler(
            statusCode=status.HTTP_400_BAD_REQUEST,
            errorCode="ER0006",
            result="SessionNotFoundError"
        )
    )

    return _app