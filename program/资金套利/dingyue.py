import websocket
# websocket-client安装库,但是导入是写websocket
import json
import time
import ccxt

ex = ccxt.binance()
ex.apiKey = ''
ex.secret = ''

class Binance_websocket():

    def __init__(self,symbol):

        self.symbol = symbol.lower() # 转成小写
        self.wss_url = "wss://stream.binance.com/stream?streams="

    def on_open(self,ws):
        print("on_open")# 连接成功

        data = {
            "method": "SUBSCRIBE",
            "params":
                [
                    "{}@depth".format(self.symbol)
                ],
            "id": 1
        }
        ws.send(json.dumps(data))#以json格式发送


    def on_close(self,ws):
        print("on_close")# 连接关闭


    def on_error(self,ws, error):
        print("on_error") # 连接错误
        print(error) # 返回错误信息


    def on_message(self,ws, msg):
        msg = json.loads(msg)  # msg 返回的是字符串要转成json格式

        if 'data' in msg: # 因为第一行不是数据，排除掉非数据的打印

            #时间戳转换
            tupTime = time.localtime(msg['data']['E']/1000)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
            msg['data']['E']=otherStyleTime

        print(msg)
        if 'ping' in msg:
            ws.send(json.dumps({"pong": msg["ping"]})) # 收到平台发送的ping,返回pong，不然会断开



    def run(self):

        ws = websocket.WebSocketApp(self.wss_url,
                                    on_open=self.on_open,
                                    on_close=self.on_close,
                                    on_message=self.on_message,
                                    on_error=self.on_error)

        ws.run_forever(ping_interval=60)  # 间隔15秒发送一次心跳包                            )




ws  = Binance_websocket("BTCUSDT")
ws.run()