import os

import json
import logging
import datetime

import faust
import asyncio

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


@app.page('/home')
async def index(web, request):
    print(f'Here da request: {request}')
    return web.json({
        'test':'howdy'
    })

#
# @app.page('/', methods=['POST'])
# async def broadcast():
#     data = {
#         'message': "test"
#     }
#     for queue in app.clients:
#         await queue.put(data['message'])
#     return True

@app.page('/sse')
async def sse(web, request):

    # async def mystream():
    #     async for data in topic.stream():
    #         print(f'Received: {data!r}')
    #         event = ServerSentEvent(data)
    #         yield event.encode()

    queue = asyncio.Queue()
    app.clients.add(queue)

    async def send_events():
        while True:
            data = await queue.get()
            event = ServerSentEvent(data)
            yield event.encode()

    response = await web.json(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response


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

#
# @app.route('/up')
# async def up():
#     return 'Up'
#
#
# @app.websocket('/ws/start')
# async def start_websocket():
#     print("Starting")
#     socket_manager = PoloniexWS()
#     socket_manager.start_ws()
#     return await jsonify({ "response": True })


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

if __name__ == "__main__":
    logging.debug("Starting appp")
    app.main()
