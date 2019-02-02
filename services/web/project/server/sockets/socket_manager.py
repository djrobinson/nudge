import json
import time
import _thread

class SocketManager:

    def __init__(self):

        self.market = None

    # do all of the saves here
    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        print("ONOPEN")
        _thread.start_new_thread(self.market_on_open, ())

    def stop_ws(self):
        self.market_close_ws()

    def start_ws(self):
        self.market_start_ws()


    # Methods below are implemented by exchanges. Used to
    def market_start_ws(self):
        raise NotImplementedError("market_start_ws must be implemented by an exchange")

    def market_close_ws(self):
        raise NotImplmentedError("market_close_ws must be implemented by an exchange")

    def market_on_open(self):
        raise NotImplementedError("market_on_open must be implemented by an exchange")
