from kafka import KafkaConsumer

try:
    from pyspark import SparkContext, SparkConf
    from operator import add
except:
    print('error')


def create_task(words):
    conf = SparkConf().setAppName('letter count')
    sc = SparkContext(conf=conf)
    seq = words.split()
    data = sc.parallelize(seq)
    counts = data.map(lambda word: (word, 1)).reduceByKey(add).collect()
    sc.stop()
    return dict(counts)


def kafka_task():
    consumer = KafkaConsumer(bootstrap_servers='kafka:9092')
    consumer.subscribe(['dingo_topic'])
    all_msg = []
    for msg in consumer:
        print("kafka msg: ", str(msg.value))
        all_msg.append(str(msg.value))
    return dict({
        "consumer_res": all_msg
    })

