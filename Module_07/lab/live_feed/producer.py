import json
import time
import uuid
import random
from datetime import datetime, timezone
from confluent_kafka import Producer
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - Producer - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Redpanda configuration mimicking Kafka API
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "live_transactions"

def delivery_report(err, msg):
    """Callback triggered on successful or failed delivery of a message."""
    if err is not None:
        logger.error(f"Failed to deliver message: {err}")
    else:
        # Avoid printing every single message in high volume, but for learning we print some
        pass

def generate_transaction() -> dict:
    """Simulates a Point-of-Sale (POS) transaction."""
    merchants = ["Coffee Shop", "Tech Store", "Grocery", "Bookstore", "Gas Station"]
    return {
        "transaction_id": str(uuid.uuid4()),
        "merchant": random.choice(merchants),
        "amount": round(random.uniform(2.50, 500.00), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        # Use idempotence to guarantee exactly-once writing in case of network retries
        'enable.idempotence': True 
    }
    
    producer = Producer(conf)
    logger.info(f"Producing to topic '{TOPIC_NAME}' on {KAFKA_BROKER}...")

    try:
        messages_sent = 0
        while True:
            txn = generate_transaction()
            
            # Serialize JSON to bytes
            payload = json.dumps(txn).encode('utf-8')
            
            # Produce the message to Redpanda
            producer.produce(
                topic=TOPIC_NAME,
                value=payload,
                callback=delivery_report
            )
            
            # Serve the delivery callbacks
            producer.poll(0)
            
            messages_sent += 1
            if messages_sent % 100 == 0:
                logger.info(f"Successfully pushed {messages_sent} transactions...")
                
            # Simulate real-world delay between events (50ms)
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        logger.info("Stopping producer...")
    finally:
        # Ensure all queued messages are sent before shutting down
        logger.info("Flushing buffer...")
        producer.flush()

if __name__ == "__main__":
    main()
