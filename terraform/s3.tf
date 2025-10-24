resource "aws_s3_bucket" "sensor_data_bucket" {
  bucket = "your-bucket-name"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.sensor_data_bucket.bucket
}
