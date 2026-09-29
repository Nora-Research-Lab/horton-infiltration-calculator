FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY horton_infiltration_calculator.py .

EXPOSE 7860

CMD ["python", "app.py"]
