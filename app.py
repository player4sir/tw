from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import asyncio
from pyppeteer import launch

app = Flask(__name__)

global_browser = None
loop = asyncio.get_event_loop()

async def init_browser():
    global global_browser
    browser = await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, loop=loop)
    return browser

async def get_result(target_link):
    global global_browser
    if not global_browser:
        global_browser = await init_browser()

    page = await global_browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    url = "https://ssstwitter.com/"
    await page.goto(url)

    input_element = await page.waitForSelector("#main_page_text")
    await input_element.type(target_link)
    await page.click("#submit")
    await page.waitForNavigation()

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

    await page.close()

    return data_list

@app.route('/api', methods=['GET'])
def api():
    target_link = request.args.get('url', None)
    if not target_link:
        return jsonify({'error': '请提供目标链接'})

    result = loop.run_until_complete(get_result(target_link))
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
