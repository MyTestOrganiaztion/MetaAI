import re
import requests
from bs4 import BeautifulSoup as bs


def extract_urls(inputString:str):
    # 定義 URL 的正則表達式
    urlPattern = r'(https?://[^\s]+)'
    # 使用 re.split 拆分字串並保留匹配的 URL
    parts = re.split(f'({urlPattern})', inputString)
    print(parts)
    urls = {part for part in parts if re.match(urlPattern, part)}
    urls = list(urls)
    
    return urls

def get_website_content(url:str):
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    imgUrls = [ element["src"] for element in soup.find_all("img") ]
    
    return soup.get_text(), imgUrls

def replace_urls_with_text(inputString:str, url:str, websiteContent:str):
    inputString = inputString.replace(url, websiteContent)
    
    return inputString

if __name__ == "__main__":
    inputString = "這是一段文字包含一個網址 https://example.com 和其他內容。"
    urls, nonUrls = extract_urls_and_text(inputString)
    print("URLs:", urls)
    print("非URLs:", nonUrls)

    for website in urls:
        text, imgUrls = get_website_content(website)
        print(text)
        print(imgUrls)
