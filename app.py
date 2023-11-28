# 导入所需的库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

# 创建一个Flask应用
app = Flask(__name__)

# 创建一个全局变量，用于存储浏览器实例
global_driver = None

# 定义一个函数，用于初始化浏览器实例
def init_driver():
    global global_driver
    # 使用webdriver_manager自动下载并设置ChromeDriver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    # 创建Headless Chrome浏览器实例
    service = Service('/app/chromedriver')
    driver = webdriver.Chrome(service=service,options=options)
    # 设置keep_alive参数为True，保持远程连接的活跃
    driver.command_executor.keep_alive = True
    # 返回浏览器实例
    return driver

# 定义一个路由，接收目标链接作为参数，返回结果
@app.route('/api', methods=['GET'])
def api():
    # 获取目标链接
    target_link = request.args.get('url', None)
    # 如果没有提供目标链接，返回错误信息
    if not target_link:
        return jsonify({'error': '请提供目标链接'})
    # 获取全局变量
    global global_driver
    # 如果全局变量为空，初始化浏览器实例
    if not global_driver:
        global_driver = init_driver()
    # 打开网页
    url = "https://ssstwitter.com/"
    global_driver.get(url)

    # 使用显示等待，等待输入框元素出现
    wait = WebDriverWait(global_driver, 10)
    input_element = wait.until(EC.presence_of_element_located(("id", "main_page_text")))
    # 输入正确格式的链接
    input_element.clear()
    input_element.send_keys(target_link)

    # 提交表单
    global_driver.find_element("id", "submit").click()

    # 使用显示等待，等待重定向完成
    wait.until(EC.url_matches("https://ssstwitter.com/result_.*"))
    soup = BeautifulSoup(global_driver.page_source, 'html.parser')
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

    # 返回结果
    return jsonify(data_list)

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
