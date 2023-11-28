# 使用官方的Python运行时作为父镜像
FROM python:3.8-slim

# 设置工作目录为/app
WORKDIR /app

# 复制当前目录的内容到容器的/app目录
COPY . /app

# 安装requirements.txt中指定的所需软件包
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# 将端口80暴露给外部世界
EXPOSE 80

# 定义环境变量
ENV NAME World

# 当容器启动时运行index.py
CMD ["python", "index.py"]
