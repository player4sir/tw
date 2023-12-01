import logging
from flask import Flask, request, jsonify
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Configuration
TARGET_URL = "https://ssstwitter.com/"
CSS_SELECTOR_TEXT_INPUT = "#main_page_text"
CSS_SELECTOR_SUBMIT_BUTTON = "#submit"

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
global_browser = None
loop = asyncio.get_event_loop()

async def init_browser():
    global global_browser
    try:
        browser = await launch(
            headless=True,
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            loop=loop,
            executablePath=os.environ.get('PUPPETEER_EXECUTABLE_PATH'),
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        return browser
    except Exception as e:
        logger.error(f"Error initializing browser: {e}")
        raise

async def scrape_page(page, target_link):
    try:
        await page.goto(TARGET_URL)
        await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        input_element = await page.waitForSelector(CSS_SELECTOR_TEXT_INPUT)
        await input_element.type(target_link)

        await page.click(CSS_SELECTOR_SUBMIT_BUTTON)
        
        # Add a delay before waitForNavigation to allow time for the redirection
        await  asyncio.sleep(5)
        
        regex = r"^https://ssstwitter.com/result_.+$"
        # 等待页面的 URL 匹配正则表达式，或者超过 30 秒
        await page.waitForFunction(f"() => window.location.href.match('{regex}')", timeout=30000)

        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        result_overlay_div = soup.find('div', class_='result_overlay')

        data_list = []
        if result_overlay_div:
            all_links = result_overlay_div.find_all('a')
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                data_list.append({'res': text, 'link': href})
        else:
            data_list.append({'error': '未找到包含目标<a>元素的<div>元素'})

        return data_list
    except Exception as e:
        logger.error(f"Error in scrape_page: {e}")
        raise
    finally:
        await page.close()

async def get_result(target_link):
    global global_browser
    if not global_browser:
        global_browser = await init_browser()

    page = await global_browser.newPage()
    result = await scrape_page(page, target_link)
    return result

@app.route('/api', methods=['GET'])
def api():
    target_link = request.args.get('url', None)
    if not target_link:
        return jsonify({'error': '请提供目标链接'})

    result = loop.run_until_complete(get_result(target_link))
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
