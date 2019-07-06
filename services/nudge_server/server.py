import os

import json
import logging

import faust
import asyncio
import codecs

from datetime import datetime
from aiohttp import web

import websockets
from mode import Service
from websockets.exceptions import ConnectionClosed
from websockets.server import WebSocketServerProtocol

from sockets.exchanges.poloniex_socket import PoloniexWS

queue = []

class Websockets(Service):

    def __init__(self, app, bind ='127.0.0.1', port = 5000, **kwargs):
        self.app = app
        self.bind = bind
        self.port = port
        self.clients = set()
        super().__init__(**kwargs)

    async def register(self, ws):
        logging.info('We on register')
        self.clients.add(ws)

    async def on_message(self, ws, message):
        logging.info( "ON MESSAGE", message)
        await ws.send(message)

    async def on_messages(self,
                          ws: WebSocketServerProtocol,
                          path: str) -> None:
        print('yo got a message right here dooooeeee')
        await self.register(ws)
        logging.info('We getting to onmessage?')
        try:
            await ws.send('haldo')
        except ConnectionClosed:
            logging.info('We at on close')
            await self.on_close(ws)
        except asyncio.CancelledError:
            pass

    async def on_close(self, ws):
        # called when websocket socket is closed.
        logging.info('WS close')

    @Service.task
    async def _background_server(self):
        logging.info("When is background server called")
        await websockets.serve(self.on_messages, self.bind, self.port)

class App(faust.App):
   def on_init(self):
       logging.info("What is init dependencies")
       self.ws = Websockets(self)

   async def on_start(self):
       await self.add_runtime_dependency(self.ws)

app = App(
    'testtopic1',
    broker='kafka://kafka:9092'
)
topic = app.topic(
    'testtopic1'
)


@app.agent(topic)
async def testmeister(messages):
    print('Faust cb is called')
    async for msg in messages:
        print('About to put to queue')
        queue.append(msg)

@app.page('/example')
async def example(web, request):
    f = codecs.open("templates/index.html", 'r', 'utf-8')
    f_text = f.read()
    return web.html(f_text)


@app.page('/ws/start')
async def start_websocket(web, request):
    print("Starting")
    socket_manager = PoloniexWS()
    socket_manager.start_ws()
    return await web.json({ "response": True })


class ServerSentEvent:

    def __init__(
            self,
            data: str,
            *,
            event: str=None,
    ) -> None:
        self.data = data
        self.event = event

    def encode(self) -> bytes:
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        message = f"{message}\r\n\r\n"
        return message.encode('utf-8')

@app.page('/test')
async def test(self, request):
    return web.Response(text="haldo")


if __name__ == "__main__":
    logging.info("Starting appp")
    asyncio.ensure_future(app.ws._background_server)
    app.main()

