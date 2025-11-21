FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from the app directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Tells Flask which file contains the application
ENV FLASK_APP=app.py

# Run the application
CMD ["python", "app.py"]