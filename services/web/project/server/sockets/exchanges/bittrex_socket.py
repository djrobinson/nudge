from time import sleep
from bittrex_websocket import BittrexSocket, BittrexMethods

from server.sockets.base_socket import BaseSocket


class BittrexWS(BaseSocket):

    def __init__(self):
        BaseSocket.__init__(self)
        self.market = "Bittrex"
        self.ws = None

    def market_start_ws(self):

        on_message = self.on_message
        class MySocket(BittrexSocket):

            def on_public(self, msg):
                # Create entry for the ticker in the trade_history dict
                if msg['invoke_type'] == BittrexMethods.SUBSCRIBE_TO_EXCHANGE_DELTAS:
                    if msg['M'] not in trade_history:
                        trade_history[msg['M']] = []
                    # Add history nounce
                    trade_history[msg['M']].append(msg)
                    on_message('[Trades]: {}'.format(msg))

        # Create container
        trade_history = {}
        # Create the socket instance
        ws = MySocket()
        # Enable logging
        ws.enable_log()
        # Define tickers
        tickers = ['BTC-ETH', 'BTC-NEO', 'BTC-ZEC', 'ETH-NEO', 'ETH-ZEC']
        # Subscribe to trade fills
        ws.subscribe_to_exchange_deltas(tickers)

        while len(set(tickers) - set(trade_history)) > 0:
            sleep(1)
        else:
            for ticker in trade_history.keys():
                self.on_message('Printing {} trade history.'.format(ticker))
                for trade in trade_history[ticker]:
                    self.on_message("trades %s " % trade)

    def market_init(self):
        print("init")

    def market_on_open(self):
        print("open")

    def market_parse_message(self, msg):
        # {'M': 'BTC-NEO', 'N': 359942, 'Z': [], 'S': [{'TY': 0, 'R': 0.00213594, 'Q': 548.601}, {'TY': 1, 'R': 0.00213712, 'Q': 0.0}], 'f': [], 'invoke_type': 'SubscribeToExchangeDeltas'}
        print("parse")

    def market_close_ws(self):
        print("close")