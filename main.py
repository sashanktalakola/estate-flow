import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# Loading env variables
USERNAME = os.getenv("USER_NAME") # Don't use USERNAME env variable. It represents logged in linux user.
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")


# Brightdata authentication data
AUTH = f'{USERNAME}:{PASSWORD}'
SBR_WS_CDP = f'wss://{AUTH}@{HOST}:{PORT}'

HOMEPAGE_URL = "https://zoopla.co.uk"

# Main scraper function
async def run(pw):
    logging.debug('Connecting to Scraping Browser...')
    # browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    browser = await pw.chromium.launch(headless=False)
    try:
        page = await browser.new_page()
        logging.debug(f'Connected! Navigating to {HOMEPAGE_URL}')
        await page.goto(HOMEPAGE_URL)

        # logging.debug("Navigated! Scraping web page")
        # html = await page.content()
        # print(html)

        # Property location input
        await page.fill('input[name="autosuggest-input"]', "Glasgow")
        await page.keyboard.press("Enter")
        await page.wait_for_load_state("load")

        logging.debug("Queried location - Glasgow")

        regularListings = await page.inner_html('div[data-testid="regular-listings"]')
        soup = BeautifulSoup(await page.content(), features="html.parser")

        for i, listing in enumerate(soup.find_all("div", class_="dkr2t86")):
            pass


    finally:
        await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

if __name__ == '__main__':
    asyncio.run(main())