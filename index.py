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

    # 尝试提取视频信息
    try:
        # 创建一个 yt-dlp 下载器对象
        # 注意: 使用明文密码不安全，建议使用更安全的认证方法，如 OAuth 或 API 密钥
        ydl = yt_dlp.YoutubeDL({})
        
        info = ydl.extract_info(url, download=False)
        
        # Check if the content is marked as NSFW
        if 'NSFW' in info.get('tags', []):
            # 如果是 NSFW 的内容，重新创建 ydl 对象，传入用户名和密码的参数
            ydl = yt_dlp.YoutubeDL({'username': 'mrili15', 'password': 'ml12345601'})
            # 重新提取视频信息，使用备用端点，忽略 SSL 证书的验证
            info = ydl.extract_info(url, download=False, nocheckcertificate=True, extractor_args={'twitter': 'api=syndication'}) # 添加 extractor_args 参数
            return jsonify({'error': 'This content is marked as NSFW'})
        
        # 过滤掉包含"hls"的格式
        filtered_formats = [f for f in info['formats'] if 'hls' not in f['format']]

        # 返回一个 JSON 格式的响应，包含视频的元数据和下载链接
        return jsonify({
            'title': info['title'],
            'duration': info['duration'],
            'formats': [{'format': f['format'], 'url': f['url']} for f in filtered_formats]
        })

    except yt_dlp.utils.DownloadError as e:
        # 如果出现其他下载错误，返回一个错误信息
        return jsonify({'error': str(e)})

# 运行应用
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)



