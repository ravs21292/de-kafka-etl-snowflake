import os

# Kafka Configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'b-1.msk-cluster.xxxxxx.kafka.amazonaws.com:9092')
KAFKA_TOPIC = "sensor_readings"

# Snowflake Configurations
SNOWFLAKE_CONFIG = {
    "user": os.getenv('SNOWFLAKE_USER', 'yourusername'),
    "password": os.getenv('SNOWFLAKE_PASSWORD', 'yourpassword'),
    "account": os.getenv('SNOWFLAKE_ACCOUNT', 'youraccount.snowflakecomputing.com'),
    "warehouse": os.getenv('SNOWFLAKE_WAREHOUSE', 'sensor_etl_warehouse'),
    "database": os.getenv('SNOWFLAKE_DATABASE', 'sensor_data'),
    "schema": os.getenv('SNOWFLAKE_SCHEMA', 'public')
}

# AWS Glue Configurations (for running jobs)
AWS_GLUE_CONFIG = {
    "role_arn": "arn:aws:iam::123456789012:role/AWSGlueServiceRole",
    "script_location": "s3://your-bucket-name/scripts/glue_producer.py"
}
