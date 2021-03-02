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
    return static_file('logs.html', root='./html/')  # 静态文件


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6008, server=GeventWebSocketServer)
