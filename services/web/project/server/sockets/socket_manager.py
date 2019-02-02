import websocket
import _thread
import time
import json


class SocketManager:

    def __init__(self):
        self.ws = None

    def on_message(self, message):
        print(message)

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        print("ONOPEN")
        payload = json.dumps({'command':'subscribe','channel':'BTC_XMR'})
        _thread.start_new_thread(self.ws.send(payload), ())

    def stop_ws(self):
        self.ws.close()


    def start_ws(self):
        print("Starting Websocket 1")
        websocket.enableTrace(True)
        print("Starting Websocket 2")
        self.ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()