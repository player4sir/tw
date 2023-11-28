# 使用官方的Python运行时作为父镜像
FROM python:3.10.6

# 设置工作目录为/app
WORKDIR /app

# 复制当前目录的内容到容器的/app目录
COPY . /app
# 安装requirements.txt中指定的所需软件包
RUN pip install --no-cache-dir -r requirements.txt


# 当容器启动时运行index.py
CMD ["python", "app.py"]
