import os
from flask import Flask, request, render_template, abort
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
users = {}  # 连接进来的WebSocket客户端集合（按应用区分）
users_key = []  # 供用户选择要查看那个应用的日志


@app.route('/logs/websocket/<string:application>/<string:component>')
def logs_websocket(application, component):
    wsock = request.environ.get('wsgi.websocket')
    # 判断这个应用是否已存在，不存在时就创建应该新集合
    if not users.__contains__(application):
        users[application] = set()
        users_key.append(application)
        print('应用 {0} 完成注册, 客户端集合已创建!'.format(application))
    users[application].add(wsock)
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            message = wsock.receive()  # 接收客户端发来的信息
        except Exception:
            break
        if message:
            for user in users[application]:
                try:
                    # 给客户端推送信息
                    user.send('{0}> {1}'.format(component, message))
                except Exception:
                    break  # 客户端已断开连接
    users[application].remove(wsock)  # 如果有客户端断开，则删除这个断开的WebSocket
    return 'Client has broken the connection.'


@app.route('/logs/view/<string:application>')
def logs(application):
    web_socket_host = os.environ.get('LOG_WEBSOCKET', 'localhost:6008')
    if application in users_key:
        app_name = application
    else:
        app_name = None
    return render_template('logs.html', web_socket_host=web_socket_host, users_key=users_key, application=app_name)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(
        ("0.0.0.0", 6008), app, handler_class=WebSocketHandler)
    server.serve_forever()
