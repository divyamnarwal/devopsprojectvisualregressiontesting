FROM python:3.12-slim

# Purpose: container image for running API + visual regression utilities.
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main/api/server.py"]
