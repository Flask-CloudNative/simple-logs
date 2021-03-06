FROM python:3.8.7
WORKDIR /app
ADD . /app
ENV LOG_WEBSOCKET=localhost:6008
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]
EXPOSE 6008