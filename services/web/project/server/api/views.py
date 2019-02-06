# services/web/server/api/views.py

import redis
import json
from rq import Queue, push_connection, pop_connection
from flask import current_app, render_template, Blueprint, jsonify, request

from server.tasks.tasks import create_task
from server.sockets.exchanges.poloniex_socket import PoloniexWS
from server.sockets.exchanges.bittrex_socket import BittrexWS
from server.sockets.exchanges.binance_socket import BinanceWS

from kafka import KafkaProducer, KafkaConsumer, TopicPartition

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


@main_blueprint.route('/kafka_consumer', methods=['GET'])
def kafka_consumer():
    consumer = KafkaConsumer(bootstrap_servers='kafka:9092')
    consumer.subscribe(['dingo_topic'])
    all_msg = []
    return jsonify({
        "consumer_res": all_msg
    })

@main_blueprint.route('/test_kafka', methods=['GET'])
def test_kafka():
    producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('dingo_topic', { 'test': 'some arguments'})
    return jsonify({
        "khafka_response": "sent"
    })




