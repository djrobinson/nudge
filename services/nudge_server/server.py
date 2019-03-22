import os

import json
import logging

import faust
import asyncio
import codecs

from datetime import datetime
from aiohttp import web

from functools import partial

from aiohttp_sse import EventSourceResponse, sse_response

import aiohttp_cors

from sockets.exchanges.poloniex_socket import PoloniexWS


app = faust.App(
    'testtopic1',
    broker='kafka://kafka:9092'
)
topic = app.topic(
    'testtopic1'
)

queue = asyncio.Queue()

async def mysink(stream):
    async for event in stream:
        print(f'AGENT YIELD: {value!r}')
        yield event

@app.agent(topic, sink=[mysink])
async def testmeister(messages):
    print('Faust cb is called')
    async for msg in messages:
        print('About to put to queue')
        yield msg


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

@app.page('/sse')
async def sse(self, request):

    print('What is SSEs')
    async with sse_response(request) as resp:
        while True:
            # data = await mysink()
            data = 'Server Time : {}'.format(datetime.now())
            print(data)
            await resp.send(data)
            await asyncio.sleep(1.0)
    return resp



# Below handles any requests made from FE as Faust doesn't allow CORS

aiohttp_app = app.web.web_app
cors = aiohttp_cors.setup(aiohttp_app)

print("What is router: %s" % str(aiohttp_app.router.resources))

resources = aiohttp_app.router.resources()
for resource in resources:
    print("What is resource: %s " % resource.__dict__.keys())
    cors.add(resource)

if __name__ == "__main__":
    logging.debug("Starting appp")

    app.main()
