import logging
import datetime

import faust
import asyncio

from quart import Quart, websocket, jsonify, make_response
from quart_cors import cors

from sockets.exchanges.poloniex_socket import PoloniexWS


app = Quart(__name__)
app = cors(app)

app.clients = set()


@app.route('/')
async def index():
    logging.info("calling")
    return jsonify([1, 2])


@app.route('/sse')
async def sse():
    faust_app = faust.App(
        'TestMeister',
        broker='kafka:9092'
    )
    topic = faust_app.topic('TestMeister')
    await faust_app.start()

    @asyncio.coroutine
    async def send_events():
        async for event in topic.stream():
            yield event.encode()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_events())

    response = await make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )


    response.timeout = None
    return response


@app.route('/up')
async def up():
    return 'Up'

@app.websocket('/ws')
async def ws():
    logging.info("Websocket called")
    while True:
        data = await websocket.receive()
        logging.debug('What is data: ', data)
        await websocket.send(f"echo {data}")

@app.websocket('/ws/faust')
async def faust_ws():
    while True:
        faust_app = faust.App(
            'nudgeapp',
            broker='kafka:9092',
            value_serializer='raw',
        )

        test_topic = faust_app.topic('TestMeister')

        @faust_app.agent(test_topic)
        async def testing_faust_stream(messages):
            async for msg in messages:
                await websocket.send(f"MESSAGES: {msg}")





@app.websocket('/ws/start')
async def start_websocket():
    print("Starting")
    socket_manager = PoloniexWS()
    socket_manager.start_ws()
    return await jsonify({ "response": True })


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
    app.run()
