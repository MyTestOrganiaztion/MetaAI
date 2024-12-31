import requests
import base64

def get_base64(url:str):
    return base64.b64encode(requests.get(url).content)


if __name__ == "__main__":
    url = "https://img.skmbuy.com.tw/App_Images/727/Page/2024/1011/3f71b1b7-feac-41ce-92fd-e9dffc250b2e.jpg.webp"
    print(get_base64(url))