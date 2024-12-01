from confluent_kafka import Producer

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address
}

# Initialize the producer
producer = Producer(producer_config)

# Callback function to check for delivery success/failure
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produce a message
topic = 'test-topic'
message = 'Hello Kafka!'
producer.produce(topic, message, callback=delivery_report)

# Wait for any outstanding messages to be delivered
producer.flush()
