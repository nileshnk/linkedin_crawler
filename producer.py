from confluent_kafka import Producer
from dotenv import load_dotenv
load_dotenv()
import os

# Kafka producer configuration
kafka_host = os.getenv("KAFKA_HOST")
kafka_port = os.getenv("KAFKA_PORT")

producer_config = {
    'bootstrap.servers': f'{kafka_host}:{kafka_port}'  # Kafka broker address
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
producer.produce(topic, message, callback=delivery_report)

def ProduceData(topic, message):
    producer.produce(topic, message, callback=delivery_report)
    
# Wait for any outstanding messages to be delivered
def Flush():
    producer.flush()