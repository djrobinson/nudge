import os
import time
from server.sockets.base_socket import BaseSocket

import time
from binance.client import Client # Import the Binance Client
from binance.websockets import BinanceSocketManager # Import the Binance Socket Manager


class BinanceWS(BaseSocket):

    def __init__(self):
        BaseSocket.__init__(self)
        self.market = 'Binance'
        self.bm = None
        self.conn_key = None

    def market_start_ws(self):
        PUBLIC = os.getenv('BINANCE_PUBLIC')
        SECRET = os.getenv('BINANCE_SECRET')

        # Instantiate a Client
        self.ws = Client(api_key=PUBLIC, api_secret=SECRET)

        # Instantiate a BinanceSocketManager, passing in the client that you instantiated
        self.bm = BinanceSocketManager(self.ws)

        # This is our callback function. For now, it just prints messages as they come.
        def handle_message(msg):
            print(msg)

        # Start trade socket with 'ETHBTC' and use handle_message to.. handle the message.
        self.conn_key = self.bm.start_trade_socket('ETHBTC', handle_message)
        # then start the socket manager
        self.bm.start()

        time.sleep(10)



    def market_close_ws(self):
        # stop the socket manager
        bm = self.bm
        bm.close()

    def market_init(self):
        print("mkt init")

    def market_on_open(self):
        print("open")

    def market_parse_message(self, msg):
        # {'e': 'trade', 'E': 1549338783436, 's': 'ETHBTC', 't': 105446337, 'p': '0.03098000', 'q': '2.67500000', 'b': 274075944, 'a': 274085370, 'T': 1549338783428, 'm': True, 'M': True}
        print("parse")
