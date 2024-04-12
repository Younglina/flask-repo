FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app/flask/
RUN  apt-get update && \
      rm -rf /var/lib/apt/lists/*
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# 设置启动命令为运行Flask应用
# CMD ["flask", "run"]
RUN chmod +x /app/flask/init.sh
ENTRYPOINT ["/app/flask/init.sh"]