import json

from openai import RateLimitError, APIConnectionError, APITimeoutError, AuthenticationError, PermissionDeniedError
from fastapi import Response, status


def formatResponse(result:str|list|dict, *, code:str="OK000", detail:str=None):
    if not isinstance(result, str):
        result = json.dumps(result)
    
    return {
        "code": code,
        "detail": detail,
        "result": result
    }

def error_handler(func):
    def wrapper(*args, **kwargs):
        response:Response = args[0]
        while True:
            try:
                result =  func(*args, **kwargs)
                return formatResponse(result)

            except RateLimitError as e:
                # 請求超出限制，等待一段時間後重試
                print(f"RateLimitError: {e}.")
                response.status_code = e.status_code
                return formatResponse("RateLimitError", code="ER000", detail=e.message)

            except APIConnectionError as e:
                # 網絡問題或無法連接到 OpenAI 服務器
                print(f"APIConnectionError: {e}. Retrying in 5 seconds...")
                response.status_code = status.HTTP_400_BAD_REQUEST
                return formatResponse("APIConnectionError", code="ER001", detail=e.message)
            
            except APITimeoutError as e:
                # 請求超時
                print(f"APITimeoutError: {e}. Retrying in 5 seconds...")
                response.status_code = status.HTTP_408_REQUEST_TIMEOUT
                return formatResponse("APITimeoutError", code="ER002", detail=e.message)

            except AuthenticationError as e:
                # 無效的 API 金鑰
                print(f"AuthenticationError: {e}. Please check your API key.")
                response.status_code = e.status_code
                return formatResponse("AuthenticationError", code="ER003", detail=e.message)
            
            except PermissionDeniedError as e:
                # 沒有權限使用 OpenAI 服務
                print(f"PermissionDeniedError: {e}. Please check your permissions.")
                response.status_code = e.status_code
                return formatResponse("PermissionDeniedError", code="ER004", detail=e.message)
    
    return wrapper