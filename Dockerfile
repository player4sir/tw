FROM python:3.10

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 创建一个工作目录
WORKDIR /app

# 复制代码到容器中
COPY . .

RUN pip install -r requirements.txt
ENV PYPPETEER_CHROMIUM_REVISION=800071
ENV PYPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome

# 映射端口
EXPOSE 5000

RUN pip install gunicorn

# 运行应用
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
