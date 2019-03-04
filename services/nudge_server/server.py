import logging
import datetime

import faust

from quart import Quart, websocket, jsonify
from quart_cors import cors

from sockets.exchanges.poloniex_socket import PoloniexWS


app = Quart(__name__)
app = cors(app)


@app.route('/')
async def index():
    logging.info("calling")
    return jsonify([1, 2])


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

if __name__ == "__main__":
    logging.debug("Starting appp")
    app.run()
