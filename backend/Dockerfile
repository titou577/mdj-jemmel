FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed for SQLite (usually already in python image)
RUN pip install --no-cache-dir --upgrade pip

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Cloud Run expects listening on $PORT (default 8080)
# Use gunicorn to serve the Flask app
ENV PORT=8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]