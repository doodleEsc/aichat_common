FROM python:3.12-slim-bullseye

WORKDIR /app/src

# 安装 uv
RUN pip install uv

# 配置 uv 使用清华源
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# Copying actual application
COPY . .

# Installing requirements using uv
RUN uv pip install --system --no-cache-dir .

CMD ["/usr/local/bin/python", "-m", "aichat_common"]
