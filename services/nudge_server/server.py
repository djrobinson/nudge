import os

import json
import logging

import faust
import asyncio
import codecs

from datetime import datetime

from aiohttp_sse import sse_response

import aiohttp_cors

from objects.kafka.market_consumer import MarketConsumer
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
    print('Faust cb is called')
    async for msg in messages:
        print(msg)
        for queue in app.clients:
            await queue.put(msg)


@app.page('/')
async def index(web, request):
    f = codecs.open("nudge_client/build/index.html", 'r', 'utf-8')
    f_text = f.read()
    return web.html(f_text)

@app.page('/example')
async def example(web, request):
    f = codecs.open("templates/index.html", 'r', 'utf-8')
    f_text = f.read()
    return web.html(f_text)

@app.page('/sse')
async def sse(web, request):

    queue = asyncio.Queue()
    app.clients.add(queue)

    async with sse_response(request) as resp:
        while True:
            data = await queue.get()
            event = ServerSentEvent(data)
            print("Event-o %s" % event)
            await resp.send(data)

    return resp


# @app.route('/show_transactions')
# async def show_transactions():
#     api_call_time = datetime.datetime.now()
#     api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
#     print("show_transactions API request made at " + api_call_time)
#     market = MarketConsumer('kafka:9092', 'testtopic1')
#     transaction_list = await market.consume_all_messages()
#     if len(transaction_list) == 0:
#         return "Kafka Topic is empty"
#     a = []
#     for i in transaction_list:
#         a.append(json.loads(i))
#     transactions = a
#     return jsonify(transactions)


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


cors = aiohttp_cors.setup(app)

async def test(web, request):
    return "haldo"

resource = cors.add(app.router.add_resource("/test"))
route = cors.add(
    resource.add_route("GET", test), {
        "http://client.example.org": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers=("X-Custom-Server-Header",),
            allow_headers=("X-Requested-With", "Content-Type"),
            max_age=3600,
        )
    })


if __name__ == "__main__":
    logging.debug("Starting appp")
    app.main()
