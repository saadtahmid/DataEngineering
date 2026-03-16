import json
from datetime import datetime, timezone
import time
from confluent_kafka import Consumer, KafkaError
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - Consumer - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "live_transactions"
# 5 seconds Tumbling Window
WINDOW_DURATION_SECONDS = 5.0  

def is_window_expired(start_time: float) -> bool:
    return (time.time() - start_time) >= WINDOW_DURATION_SECONDS

def print_window_aggregation(window_start: datetime, total_revenue: float, count: int, merchants: dict):
    logger.info("=" * 40)
    logger.info(f"TUMBLING WINDOW FIRED: {window_start.strftime('%H:%M:%S')} - {datetime.now(timezone.utc).strftime('%H:%M:%S')}")
    logger.info(f"TOTAL REVENUE: ${total_revenue:,.2f}")
    logger.info(f"TOTAL TRANSACTIONS: {count}")
    logger.info("Top Merchants:")
    for m, amt in sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:3]:
        logger.info(f"  - {m}: ${amt:,.2f}")
    logger.info("=" * 40)

def main():
    conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'real_time_metrics_app',
        'auto.offset.reset': 'latest',  # Only care about new data arriving
    }

    consumer = Consumer(conf)
    consumer.subscribe([TOPIC_NAME])
    logger.info(f"Subscribed to topic '{TOPIC_NAME}'. Waiting for data...")

    # Aggregation State
    window_start_time = time.time()
    window_start_dt = datetime.now(timezone.utc)
    
    current_revenue = 0.0
    current_count = 0
    merchant_sales = {}

    try:
        while True:
            # Poll for new messages 
            msg = consumer.poll(timeout=1.0)
            
            # Check if tumbling window expired (even if no message came in)
            if is_window_expired(window_start_time):
                if current_count > 0:
                    print_window_aggregation(window_start_dt, current_revenue, current_count, merchant_sales)
                
                # Reset State for the next Tumbling Window
                window_start_time = time.time()
                window_start_dt = datetime.now(timezone.utc)
                current_revenue = 0.0
                current_count = 0
                merchant_sales = {}

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    continue

            # Parse and aggregate payload
            try:
                payload = json.loads(msg.value().decode('utf-8'))
                amount = float(payload.get("amount", 0.0))
                merchant = payload.get("merchant", "Unknown")

                # Accumulate state
                current_revenue += amount
                current_count += 1
                merchant_sales[merchant] = merchant_sales.get(merchant, 0.0) + amount

            except Exception as e:
                logger.error(f"Failed to process message: {e}")

    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
