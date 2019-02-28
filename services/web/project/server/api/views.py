# services/web/server/api/views.py

import json
import datetime
from quart import websocket, render_template, Blueprint, jsonify

from server.sockets.exchanges.poloniex_socket import PoloniexWS

from server.objects.kafka.market_consumer import MarketConsumer


main_blueprint = Blueprint('tasks', __name__,)

@main_blueprint.route('/websockets/start', methods=['GET'])
async def start_websocket():
    print("Starting")
    socket_manager = PoloniexWS()
    socket_manager.start_ws()
    return await jsonify({ "response": True })


@main_blueprint.route('/websockets/stop', methods=['GET'])
async def stop_websocket():
    print("Stoppsing")
    socket_manager = PoloniexWS()
    socket_manager.stop_ws()
    return jsonify({ "response": True })


@main_blueprint.route('/test_faust', methods=['GET'])
async def test_faust():
    api_call_time = datetime.datetime.now()
    api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Test Faust request made at " + api_call_time)
    market = MarketConsumer('kafka:9092', 'TestMeister')
    market.test_faust()
    return "Testing Faust  Called"


@main_blueprint.route('/show_transactions', methods=['GET'])
async def show_transactions():
    api_call_time = datetime.datetime.now()
    api_call_time = api_call_time.strftime("%Y-%m-%d %H:%M:%S")
    print("show_transactions API request made at " + api_call_time)
    market = MarketConsumer('kafka:9092', 'TestMeister')
    transaction_list = market.consume_some(10)
    if len(transaction_list) == 0:
        return "Kafka Topic is empty"
    a = []
    for i in transaction_list:
        a.append(json.loads(i))
    transactions = a
    return jsonify(transactions)