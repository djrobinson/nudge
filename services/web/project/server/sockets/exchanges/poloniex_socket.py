import websocket
import json

from server.sockets.base_socket import BaseSocket

class PoloniexSocket(BaseSocket):

    def __init__(self):
        BaseSocket.__init__(self)
        self.market = "Poloniex"
        self.socket_url = "wss://api2.poloniex.com/"
        self.ws = None


    def market_start_ws(self):
        websocket.enableTrace(True)
        print("Starting Websocket 2")
        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def market_close_ws(self):
        self.ws.close()

    def market_init(self):
        payload = json.dumps({'command': 'subscribe', 'channel': 'BTC_XMR'})
        self.ws.send(payload)


