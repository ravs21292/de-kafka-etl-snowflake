import json
import snowflake.connector
from kafka import KafkaConsumer

# Snowflake config
SNOWFLAKE_CONFIG = {
    "user": "yourusername",
    "password": "yourpassword",
    "account": "youraccount.snowflakecomputing.com",
    "warehouse": "sensor_etl_warehouse",
    "database": "sensor_data",
    "schema": "public"
}

consumer = KafkaConsumer(
    'sensor_readings',
    bootstrap_servers=['b-1.msk-cluster.xxxxxx.kafka.amazonaws.com:9092'],
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

# Consume Kafka messages
for message in consumer:
    record = message.value
    try:
        cursor.execute("""
            INSERT INTO public.sensors (timestamp, temperature, pressure)
            VALUES (%s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (record['timestamp'], record['temperature'], record['pressure']))
        conn.commit()
    except Exception as e:
        print(f"Insert error: {e}")
        conn.rollback()

cursor.close()
conn.close()
