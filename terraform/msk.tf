resource "aws_msk_cluster" "sensor_data_cluster" {
  cluster_name           = "sensor-data-cluster"
  kafka_version          = "2.8.0"
  number_of_broker_nodes = 2
  broker_node_group_info {
    instance_type = "kafka.m5.large"
    client_subnet_ids = ["subnet-xxxxxx"]
    security_groups  = ["sg-xxxxxx"]
  }
}

output "msk_bootstrap_servers" {
  value = aws_msk_cluster.sensor_data_cluster.bootstrap_servers
}
