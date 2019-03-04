import logging
from quart import Quart, websocket, jsonify
from quart_cors import cors

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
        await websocket.send(f"echo {data}")


if __name__ == "__main__":
    logging.info("Starting appp")
    app.run()
