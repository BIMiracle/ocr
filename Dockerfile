# Dockerfile
FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 创建目录结构
RUN mkdir -p /app/frontend/dist

# 复制后端文件和构建后的前端
COPY main.py wcocr.cpython-312-x86_64-linux-gnu.so /app/
COPY wx /app/wx
COPY frontend/dist /app/frontend/dist

# 安装Python依赖
WORKDIR /app
RUN pip install flask

# 设置环境变量
ENV FLASK_STATIC_FOLDER=/app/frontend/dist

EXPOSE 5000

CMD ["python", "main.py"]