from kafka import KafkaProducer
import json, os

BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "scrape_tasks")

producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def enqueue_url(url: str, meta: dict | None = None):
    payload = {"url": url, "meta": meta or {}}
    producer.send(TOPIC, payload)
    producer.flush()
