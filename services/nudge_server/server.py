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

app.clients = set()


@app.agent(topic)
async def testmeister(messages):
    channel = app.channel()
    print('Faust cb is called')
    async for msg in messages:
        print('About to put to queue')
        await channel.put(msg)


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


async def test(request):
    return web.Response(text="haldo")


@app.page('/sse')
async def sse(web, request):
    channel = app.channel()
    print('SSES GETTING TO GOING')
    async with sse_response(request) as resp:
        async for event in channel:
            if event is None:
                break
            await resp.send("EVENT: %s" % event)

    return resp


# Below handles any requests made from FE as Faust doesn't allow CORS

aiohttp_app = app.web.web_app
cors = aiohttp_cors.setup(aiohttp_app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

resource = cors.add(aiohttp_app.router.add_resource("/test"))
cors.add(
    resource.add_route("GET", test), {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })

# cors.add(aiohttp_app.router.add_route("GET", "/sse", sse))
# cors.add(aiohttp_app.router.add_route("PUT", "/sse", sse))
# cors.add(aiohttp_app.router.add_route("POST", "/sse", sse))
# cors.add(aiohttp_app.router.add_route("DELETE", "/sse", sse))

if __name__ == "__main__":
    logging.debug("Starting appp")
    app.main()
