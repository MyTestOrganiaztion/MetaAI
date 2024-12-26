import json
from openai import RateLimitError, Timeout, APIConnectionError, AuthenticationError


def response(result:str|list|dict, *, code:str="OK000", detail:str=None):
    if not isinstance(result, str):
        result = json.dumps(result)
    
    return {
        "code": code,
        "detail": detail,
        "result": result
    }

def error_handler(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result =  func(*args, **kwargs)
                return response(result)

            except RateLimitError as e:
                # 請求超出限制，等待一段時間後重試
                print(f"RateLimitError: {e}.")
                return response("RateLimitError", code="ER000", detail=e.message)

            except Timeout as e:
                # 請求超時，重試
                print(f"Timeout: {e}. Retrying...")
                return response("Timeout", code="ER001", detail=e.message)

            except APIConnectionError as e:
                # 網絡問題或無法連接到 OpenAI 服務器
                print(f"APIConnectionError: {e}. Retrying in 5 seconds...")
                return response("APIConnectionError", code="ER002", detail=e.message)

            except AuthenticationError as e:
                # 無效的 API 金鑰
                print(f"AuthenticationError: {e}. Please check your API key.")
                return response("AuthenticationError", code="ER003", detail=e.message)
    
    return wrapper