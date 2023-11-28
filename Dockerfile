FROM python:3.10.6

# 设置工作目录为/app
WORKDIR /app

# 复制当前目录的内容到容器的/app目录
COPY . /app

# 安装requirements.txt中指定的所需软件包
RUN pip install --no-cache-dir -r requirements.txt

# 下载并安装特定版本的Chrome浏览器
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_87.0.4280.88-1_amd64.deb
RUN apt-get install -y ./google-chrome-stable_87.0.4280.88-1_amd64.deb
RUN rm ./google-chrome-stable_87.0.4280.88-1_amd64.deb

# 当容器启动时运行app.py
CMD ["python", "app.py"]
