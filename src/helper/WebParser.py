import re
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse


def extract_urls(inputString:str):
    # 定義 URL 的正則表達式
    urlPattern = r'(https?://[^\s]+)'
    # 使用 re.split 拆分字串並保留匹配的 URL
    parts = re.split(f'({urlPattern})', inputString)
    # print(parts)
    urls = {part for part in parts if re.match(urlPattern, part)}
    urls = list(urls)

    nonUrls = {part for part in parts if not re.match(urlPattern, part) and part}
    nonUrls = list(nonUrls)
    
    return urls, nonUrls

def get_website_content(url:str):
    parsedUrl = urlparse(url)
    host = f"{parsedUrl.scheme}://{parsedUrl.netloc}"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    imgUrls = []
    for imgElement in soup.find_all("img"):
        src: str | None = imgElement.get("src")
        if src and src.endswith(('png', 'jpeg', 'gif', 'webp')):
            if src.startswith("http"):
                imgUrls.append(src)
            elif src.startswith("/"):
                imgUrls.append(host + src)
            elif src.startswith("./"):
                imgUrls.append(host + src[1:])

    # Extract and clean text content
    rawText = soup.get_text()
    cleanedText = " ".join(
        line.strip() for line in rawText.splitlines() if line.strip()
    )

    return cleanedText, imgUrls

def replace_urls_with_text(inputString:str, url:str, websiteContent:str):
    inputString = inputString.replace(url, f'網頁內容:"{websiteContent}"')
    
    return inputString

if __name__ == "__main__":
    inputString = "這是一段文字包含一個網址 https://example.com 和其他內容。"
    urls, nonUrls = extract_urls(inputString)
    print("URLs:", urls)

    for website in urls:
        text, imgUrls = get_website_content(website)
        print(text)
        print(imgUrls)
