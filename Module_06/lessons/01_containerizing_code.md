# Containerizing Code (Docker)

Before orchestrating jobs, we must guarantee that our code executes exactly the same way whether it's triggered on your laptop, on a team member's laptop, or on a production server.

## The Problem
"It works on my machine" is the most common failure in Data Engineering. 
If your Python script relies on `polars==1.0`, but the production server has `polars==0.18` installed, your orchestration pipeline will crash unexpectedly.

## The Solution: Dockerfiles
A `Dockerfile` is a blueprint. It tells the Docker engine exactly how to build a custom Linux image that contains your code and *only* your specific dependencies.

```dockerfile
# 1. Base Image (The OS)
FROM python:3.10-slim

# 2. Establish Working Directory
WORKDIR /app

# 3. Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy actual code
COPY . .

# 5. Default execution command
CMD ["python", "app.py"]
```

Every time you run this container, it spins up a completely isolated Linux environment, executes the `app.py` script with the exact library versions requested, and then shuts down cleanly. 

When configuring tools like Dagster, we will containerize our Dagster environment so it is fully isolated from our host laptop.
