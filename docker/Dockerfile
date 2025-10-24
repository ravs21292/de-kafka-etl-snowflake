# Use Python 3.11-slim as base image
FROM python:3.11-slim-bullseye

# Set working directory in the container
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY . .

# Set the default command for the container to run the consumer
CMD ["python3", "consumer_batch_sync.py"]
