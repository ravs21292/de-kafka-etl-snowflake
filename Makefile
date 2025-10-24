# Makefile for Kafka ETL Snowflake Project

DOCKER_COMPOSE = docker-compose
SERVICE = etl-service

.PHONY: help build up down rebuild produce consume logs shell

help:
	@echo "Usage:"
	@echo "  make build         Build all Docker images"
	@echo "  make up            Start Zookeeper, Kafka, Postgres services"
	@echo "  make down          Stop and remove all services"
	@echo "  make rebuild       Rebuild and start services (down + build + up)"
	@echo "  make produce       Run Spark CSV producer to send data to Kafka"
	@echo "  make consume       Run Kafka consumer to batch insert into Snowflake"
	@echo "  make logs          Show combined logs from all services"
	@echo "  make shell         Open psql shell inside Postgres container"

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

rebuild: down build up

produce:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) python3 etl_spark_producer.py

consume:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) python3 consumer_batch_sync.py

logs:
	$(DOCKER_COMPOSE) logs -f --tail=100

shell:
	# Find Postgres container name dynamically and exec psql shell
	docker exec -it $$(docker ps --filter ancestor=postgres:15 --format '{{.Names}}' | head -n1) psql -U postgres -d sensors
