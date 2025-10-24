import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import col
from awsglue.job import Job
from pyspark.sql import SparkSession

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(sys.argv[1], sys.argv)

# Parameters (from Glue Job)
s3_input_path = sys.argv[2]  # S3 Path to the CSV file
kafka_bootstrap_servers = sys.argv[3]  # MSK bootstrap servers
kafka_topic = sys.argv[4]  # Kafka topic to send data to

# Read CSV from S3
df = spark.read.option("header", "true").csv(s3_input_path)

# Clean and process data
df = df.dropna(subset=["temperature", "pressure"]) \
       .filter(col("temperature") < 150) \
       .withColumn("temperature", col("temperature").cast("double")) \
       .withColumn("pressure", col("pressure").cast("double"))

# Normalize pressure
pressure_min = df.agg({"pressure": "min"}).collect()[0][0]
pressure_max = df.agg({"pressure": "max"}).collect()[0][0]
df = df.withColumn("pressure", (col("pressure") - pressure_min) / (pressure_max - pressure_min))

# Convert rows to JSON strings for Kafka
json_df = df.selectExpr("CAST(timestamp AS STRING)", "CAST(temperature AS DOUBLE)", "CAST(pressure AS DOUBLE)").toJSON()

# Write to Kafka
json_df.write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("topic", kafka_topic) \
    .save()

job.commit()
