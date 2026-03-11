# Use a slim Python base image for a smaller production container.
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the application working directory.
WORKDIR /app

# Copy dependency definition first to leverage Docker layer caching.
COPY requirements.txt /app/requirements.txt

# Install Python dependencies.
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the full project source into the container.
COPY . /app

# Expose FastAPI service port.
EXPOSE 8000

# Start the FastAPI application with Uvicorn.
CMD ["uvicorn", "src.main.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
