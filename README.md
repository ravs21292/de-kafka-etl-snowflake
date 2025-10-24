# ETL Pipeline with Snowflake and AWS

This project implements an **ETL pipeline** using **AWS services** (Glue, MSK, S3, and Kafka) and **Snowflake** as the data warehouse.

## Services
- **S3**: Raw data storage
- **AWS Glue**: ETL job for processing data
- **MSK (Managed Kafka)**: Kafka for message streaming
- **Snowflake**: Data warehouse for processed data
- **EC2/ECS**: Kafka consumer for processing and storing data in Snowflake
- **CloudWatch**: Monitoring and alerts

## Project Setup

1. **AWS Setup**:
   - Create an S3 bucket.
   - Set up MSK (Kafka).
   - Create a Snowflake account and set up the database, schema, and tables.
   - Set up AWS Glue job to process CSV files and send to MSK.

2. **Terraform Setup**:
   - Use Terraform to provision the required AWS resources. Ensure your AWS credentials are configured in your environment.
   - Run `terraform apply` to deploy resources.

3. **Running the ETL Pipeline**:
   - Upload your CSV data to S3: `aws s3 cp sensor_data.csv s3://your-bucket-name/inputs/`
   - Trigger AWS Glue job for processing.
   - The consumer script will pull data from Kafka and insert into Snowflake.

4. **Monitoring**:
   - Logs are available in CloudWatch.
   - Kafka consumer logs and Glue job logs will be captured in CloudWatch.

## Requirements

- Terraform
- AWS CLI
- Python 3.11+
- Snowflake account
