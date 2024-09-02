import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


AUTH = f'{USERNAME}:{PASSWORD}'
SBR_WS_CDP = f'wss://{AUTH}@{HOST}:{PORT}'

HOMEPAGE_URL = "https://zoopla.co.uk"

async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print(f'Connected! Navigating to {HOMEPAGE_URL}')
        await page.goto(HOMEPAGE_URL)

        print("Navigated! Scraping web page")
        html = await page.content()
        print(html)

    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())