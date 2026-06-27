FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    g++ cmake make \
    && rm -rf /var/lib/apt/lists/*

COPY vector_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pre-compiled .so from the build stage
COPY memory_engine/build/*.so .

COPY vector_service/main.py .

EXPOSE 8001

CMD ["python", "main.py"]
