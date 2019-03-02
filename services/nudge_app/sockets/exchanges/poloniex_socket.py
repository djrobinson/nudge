import websocket
import json
import _thread

from server.sockets.base_socket import BaseSocket
from server.enums.poloniex_market_lookup import PoloniexMarketLookup


class PoloniexWS(BaseSocket):

    def __init__(self):
        BaseSocket.__init__(self)
        self.market = "Poloniex"
        self.socket_url = "wss://api2.poloniex.com/"
        self.ws = None
        self.open_channels = []


    def market_start_ws(self):
        websocket.enableTrace(True)
        print("Starting Websocket 2")
        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.market_init
        self.ws.run_forever()


    def market_close_ws(self):
        print("close")
        # self.ws.close()

    def market_init(self):
        self.open_channels.append(PoloniexMarketLookup.BTCXMR)
        ws = self.ws
        def run(*args):
            payload = json.dumps({'command': 'subscribe', 'channel': 'BTC_ETH'})
            ws.send(payload)
        _thread.start_new_thread(run, ())

    def market_parse_message(self, message):
        print("Parsing market message")
        if message[0] in self.open_channels:
            print("Start parse ", message)

    def market_on_open(self):
        print("tmp")



