import requests
from bs4 import BeautifulSoup
url = "https://www.linkedin.com/search/results/all/?keywords=teddy%20oweh&origin=GLOBAL_SEARCH_HEADER&sid=ZCT"

headers = {
    "authority": "www.linkedin.com",
    "method": "GET",
    "path": "/search/results/all/?keywords=teddy%20oweh&origin=GLOBAL_SEARCH_HEADER&sid=ZCT",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "YOUR_LONG_COOKIE_HERE",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Cookie":open("cookie.txt").read()
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(soup.prettify())