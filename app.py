# 导入所需的模块
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import yt_dlp

# 创建一个 Flask 应用和一个 API 对象
app = Flask(__name__)
api = Api(app)

# 定义一个资源类，用于处理视频网址的请求
class Video(Resource):
    def get(self):
        # 获取请求中的网址参数
        url = request.args.get('url')
        # 如果没有提供网址，返回一个错误信息
        if not url:
            return jsonify({'error': 'No url provided'})
        # 创建一个 yt-dlp 下载器对象
        ydl = yt_dlp.YoutubeDL()
        # 尝试提取视频信息
        try:
            info = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            # 如果出现错误，返回一个错误信息
            return jsonify({'error': str(e)})
        # 生成一个文件名
        filename = ydl.prepare_filename(info)
        
        # 获取最佳的音频和视频格式
        best_audio = None
        best_video = None
        for fmt in info['formats']:
            if 'audio' in fmt['format']:
                if best_audio is None or (fmt['abr'] and (not best_audio or fmt['abr'] > best_audio['abr'])):
                    best_audio = fmt
            elif 'video' in fmt['format']:
                if best_video is None or (fmt['height'] and (not best_video or fmt['height'] > best_video['height'])):
                    best_video = fmt

        # 返回一个 JSON 格式的响应，包含视频的元数据和下载链接
        response_data = {
            'title': info['title'],
            'duration': info['duration'],
            'filename': filename,
            'formats': [{'format': f['format'], 'url': f['url']} for f in info['formats']]
        }

        if best_audio and best_video:
            response_data['best_format'] = f'{best_audio["format"]} + {best_video["format"]}'
        else:
            response_data['best_format'] = 'N/A'

        return jsonify(response_data)

# 将资源类添加到 API 对象中，指定路由
api.add_resource(Video, '/api')

# 运行应用
if __name__ == '__main__':
    app.run(debug=True)
