FROM python:3.8.7
WORKDIR /app
ADD . /app
ENV LOG_WEBSOCKET=localhost
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir -r requirements.txt
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:6008", "--log-file", "-", "--access-logfile", "-", "--error-logfile", "-"]
EXPOSE 6008