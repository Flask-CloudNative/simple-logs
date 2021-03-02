import socket
from bottle import static_file, Bottle
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

app = Bottle()
users = set()  # 连接进来的WebSocket客户端集合


@app.get('/api/v1/logs/websocket', apply=[websocket])
def api_v1_logs_websocket(ws):
    users.add(ws)
    while True:
        msg = ws.receive()  # 接收客户端的信息
        if msg:
            for u in users:
                u.send(msg)  # 发送信息给所有的客户端
        else:
            break
    users.remove(ws)


@app.get('/api/v1/logs')
def api_v1_logs():
    web_socket_host = socket.gethostbyname(host_name)
    html_text = '''
    <!DOCTYPE HTML>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Simple Logs</title>
            <link rel="stylesheet" href="/api/v1/logs/static/logs.css" type="text/css" />
            <script type="text/javascript">
                var wsUrl = "ws://{0}:6008/api/v1/logs/websocket";
            </script>
            <script src="/api/v1/logs/static/logs.js" type="text/javascript" charset="utf-8"></script>
        </head>
        <body>
            <pre class="msg"><code></code></pre>
        </body>
    </html>
    '''.format(web_socket_host)
    return html_text


@app.get('/api/v1/logs/static/<path>')
def api_v1_logs_static(path):
    return static_file(path, root='./static/')  # 静态文件


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6008, server=GeventWebSocketServer)
