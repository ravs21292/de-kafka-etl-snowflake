resource "aws_glue_job" "sensor_data_etl" {
  name     = "sensor-data-etl"
  role_arn = "arn:aws:iam::123456789012:role/AWSGlueServiceRole"  # Replace with your Glue Role ARN
  command {
    name            = "glueetl"
    script_location = "s3://your-bucket-name/scripts/glue_producer.py"  # S3 location of your Glue script
  }
  max_capacity = 10
  default_arguments = {
    "--TempDir"             = "s3://your-bucket-name/temp/"
    "--job-bookmark-option" = "job-bookmark-disable"
  }
  depends_on = [aws_s3_bucket.sensor_data_bucket]
}
