
import json
import snowflake.connector
from kafka import KafkaConsumer
from config import KAFKA_BROKER, KAFKA_TOPIC, SNOWFLAKE_CONFIG

# Create Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],  # Replace with MSK bootstrap servers
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='etl-consumer-group'
)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=SNOWFLAKE_CONFIG["user"],
    password=SNOWFLAKE_CONFIG["password"],
    account=SNOWFLAKE_CONFIG["account"],
    warehouse=SNOWFLAKE_CONFIG["warehouse"],
    database=SNOWFLAKE_CONFIG["database"],
    schema=SNOWFLAKE_CONFIG["schema"]
)

cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE OR REPLACE TABLE public.sensors (
    id STRING PRIMARY KEY,
    timestamp TIMESTAMP,
    temperature FLOAT,
    pressure FLOAT
);
""")

def insert_batch(records):
    """Inserts records into Snowflake in bulk using copy from."""
    buffer_io = io.StringIO()
    for r in records:
        buffer_io.write(f"{r['timestamp']},{r['temperature']},{r['pressure']}\n")
    buffer_io.seek(0)
    cursor.copy_from(buffer_io, 'sensors', sep=",", columns=('timestamp', 'temperature', 'pressure'))
    conn.commit()

# Buffer and consume messages
buffer = []
for message in consumer:
    record = message.value
    buffer.append(record)

    if len(buffer) >= 100:  # Insert every 100 records
        insert_batch(buffer)
        print(f"Inserted {len(buffer)} records into Snowflake.")
        buffer.clear()

# Close the Snowflake connection
cursor.close()
conn.close()
