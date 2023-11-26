# 导入所需的模块
from flask import Flask, request, jsonify
import yt_dlp

# 创建一个 Flask 应用
app = Flask(__name__)

# 定义一个路由，用于处理视频网址的请求
@app.route('/video')
def video():
    # 获取请求中的网址参数
    url = request.args.get('url')
    # 如果没有提供网址，返回一个错误信息
    if not url:
        return jsonify({'error': 'No url provided'})
    # 创建一个 yt-dlp 下载器对象，使用 --cookies-from-browser 参数让 yt-dlp 从你的浏览器获取 cookie
    ydl = yt_dlp.YoutubeDL({'cookies-from-browser': 'chrome'})
    # 尝试提取视频信息
    try:
        
        
        info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        # 如果出现错误，返回一个错误信息
        return jsonify({'error': str(e)})
    # 返回一个 JSON 格式的响应，包含视频的元数据和下载链接
    return jsonify({
        'title': info['title'],
        # 'uploader': info['uploader'],
        'duration': info['duration'],
        # 修改这一行，使用列表推导式，只保留格式为 mp4 的 url
        'formats': [{'format': f['format'], 'url': f['url']} for f in info['formats'] if f['ext'] == 'mp4']
    })

# 运行应用
if __name__ == '__main__':
    app.run(debug=False)
