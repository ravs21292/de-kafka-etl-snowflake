import os

# Snowflake Credentials (store securely, preferably in AWS Secrets Manager)
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER', 'yourusername')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD', 'yourpassword')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME', 'yourusername')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD', 'yourpassword')
