FROM python:3.11-slim

WORKDIR /opt/dagster/app

# Install system dependencies if necessary
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /opt/dagster/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy our Dagster code
COPY pyproject.toml /opt/dagster/app/pyproject.toml
COPY orchestrator /opt/dagster/app/orchestrator

# Expose Dagster webserver port
EXPOSE 3000

# Default command to run Dagster Dev server 
CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-m", "orchestrator.definitions"]
