import time
import websocket

from server.sockets.base_socket import BaseSocket

class BinanceWS(BaseSocket):

    def __init__(self):
        BaseSocket.__init__(self)
        self.market = 'Binance'

    def market_start_ws(self):
        websocket.enableTrace(True)
        print("Starting Websocket 2")
        self.ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/BNBBTC@miniTicker",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def market_close_ws(self):
        self.ws.close()

    def market_init(self):
        print("mkt init")

    def market_on_open(self):
        print("open")

    def market_parse_message(self, msg):
        print("parse")

    def market_close_ws(self):
        print("close")