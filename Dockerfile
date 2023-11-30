# 使用官方的 Python 镜像作为基础镜像
FROM python:3.10.0

# 将工作目录设置为 /app
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app
COPY . /app
# 设置环境变量
ENV PYPPETEER_NO_SANDBOX=1
ENV FLASK_APP=app.py
# 安装依赖项
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    wget \
    gconf-service \
    libasound2 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -yq libglib2.0-0 libnss3 libxss1 libasound2 libatk1.0-0 libgtk-3-0 libx11-xcb1
RUN apt-get install -yq libgbm1
# 为 Flask 应用程序暴露端口 80
EXPOSE 80

# 运行 Flask 应用程序
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
