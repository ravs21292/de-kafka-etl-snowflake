output "s3_bucket_name" {
  value = aws_s3_bucket.sensor_data_bucket.bucket
}

output "msk_bootstrap_servers" {
  value = aws_msk_cluster.sensor_data_cluster.bootstrap_servers
}

output "glue_job_name" {
  value = aws_glue_job.sensor_data_etl.name
}
