import os
from flask import Flask, request, render_template
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
users = set()  # 连接进来的WebSocket客户端集合


@app.route('/logs/websocket')
def logs_websocket():
    wsock = request.environ.get('wsgi.websocket')
    users.add(wsock)
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            message = wsock.receive()  # 接收客户端发来的信息
        except Exception:
            break
        if message:
            for user in users:
                try:
                    user.send(message)  # 给客户端推送信息
                except Exception:
                    break  # 客户端已断开连接
    users.remove(wsock)  # 如果有客户端断开，则删除这个断开的WebSocket


@app.route('/logs')
def logs():
    web_socket_host = os.environ.get('LOG_WEBSOCKET', 'localhost:6008')
    return render_template('logs.html', web_socket_host=web_socket_host)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(
        ("0.0.0.0", 6008), app, handler_class=WebSocketHandler)
    server.serve_forever()
