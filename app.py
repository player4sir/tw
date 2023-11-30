from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import asyncio
from pyppeteer import launch

# 创建一个Flask应用
app = Flask(__name__)

# 创建一个全局变量，用于存储浏览器实例
global_browser = None

# 定义一个异步函数，用于初始化浏览器实例
async def init_browser():
    # 创建一个新的事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 创建一个无头浏览器实例
    # 添加一些必要的参数，例如--no-sandbox和--disable-setuid-sandbox
    browser = await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, loop=loop, args=['--no-sandbox', '--disable-setuid-sandbox'])
    
    # 返回浏览器实例
    return browser

# 定义一个异步函数，用于打开网页并获取结果
async def get_result(target_link):
    global global_browser

    # 如果全局变量为空，初始化浏览器实例
    if not global_browser:
        global_browser = await init_browser()

    # 创建一个新的浏览器页面
    page = await global_browser.newPage()
    
    # 设置用户代理
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    
    # 打开网页
    url = "https://ssstwitter.com/"
    await page.goto(url)

    # 等待输入框元素出现
    input_element = await page.waitForSelector("#main_page_text")
    
    # 输入正确格式的链接
    await input_element.type(target_link)

    # 提交表单
    await page.click("#submit")

    # 等待重定向完成
    await page.waitForNavigation()

    # 获取页面源码
    content = await page.content()
    soup = BeautifulSoup(content, 'html.parser')
    result_overlay_div = soup.find('div', class_='result_overlay')
    
    # 获取结果
    data_list = []
    if result_overlay_div:
        all_links = result_overlay_div.find_all('a')
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            data_list.append({'res': text, 'link': href})
    else:
        data_list.append({'error': '未找到包含目标<a>元素的<div>元素'})

    # 关闭页面
    await page.close()

    # 返回结果
    return data_list

# 定义一个路由，接收目标链接作为参数，返回结果
@app.route('/api', methods=['GET'])
def api():
    # 获取目标链接
    target_link = request.args.get('url', None)
    
    # 如果没有提供目标链接，返回错误信息
    if not target_link:
        return jsonify({'error': '请提供目标链接'})

    # 调用异步函数，获取结果
    result = asyncio.run(get_result(target_link))
    
    # 返回结果
    return jsonify(result)

# 运行应用
if __name__ == '__main__':
    # 添加一个参数use_reloader=False，以避免Flask应用在容器中重复启动的问题
    app.run(host='0.0.0.0', use_reloader=False)
