# services/web/server/api/views.py

import redis
import json
import datetime
from rq import Queue, push_connection, pop_connection
from flask import current_app, render_template, Blueprint, jsonify, request, Response

from server.tasks.tasks import create_task
from server.sockets.exchanges.poloniex_socket import PoloniexWS
from server.sockets.exchanges.bittrex_socket import BittrexWS
from server.sockets.exchanges.binance_socket import BinanceWS

from server.objects.kafka.market_consumer import MarketConsumer


main_blueprint = Blueprint('tasks', __name__,)

@main_blueprint.route('/', methods=['GET'])
def home():
    return render_template('main/home.html')


@main_blueprint.route('/tasks', methods=['POST'])
def run_task():
    words = request.form['words']
    q = Queue()
    task = q.enqueue(create_task, words)
    response_object = {
        'status': 'success',
        'data': {
            'task_id': task.get_id()
        }
    }
    return jsonify(response_object), 202


@main_blueprint.route('/tasks/<task_id>', methods=['GET'])
def get_status(task_id):
    q = Queue()
    task = q.fetch_job(task_id)
    if task:
        response_object = {
            'status': 'success',
            'data': {
                'task_id': task.get_id(),
                'task_status': task.get_status(),
                'task_result': task.result,
            }
        }
    else:
        response_object = {'status': 'error'}
    return jsonify(response_object)


@main_blueprint.before_request
def push_rq_connection():
    push_connection(redis.from_url(current_app.config['REDIS_URL']))


@main_blueprint.teardown_request
def pop_rq_connection(exception=None):
    pop_connection()


@main_blueprint.route('/websockets/start', methods=['GET'])
def start_websocket():
    print("Starting")
    socket_manager = PoloniexWS()
    socket_manager.start_ws()
    return jsonify({ "response": True })


@main_blueprint.route('/websockets/stop', methods=['GET'])
def stop_websocket():
    print("Stopping")
    socket_manager = PoloniexWS()
    socket_manager.stop_ws()
    return jsonify({ "response": True })


@main_blueprint.route('/show_transactions', methods=['GET'])
def show_transactions():
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

