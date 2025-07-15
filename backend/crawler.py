import aiohttp
from bs4 import BeautifulSoup

async def crawl_webpage(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                    return ""
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text(" ", strip=True)
                return text
    except Exception as e:
        print(f"Crawling error: {str(e)}")
        return ""
