# Base image
FROM python:3.13-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser

# Working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY docs ./docs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Start application
CMD ["python", "app.py"]
