# Base image
FROM python:3.10

# Working directory
WORKDIR /Shop

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd --no-install-recommends

# Install Python dependencies
COPY requirements.txt /Shop/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /Shop/

# Create and set permissions for static and media folders
RUN mkdir -p /Shop/staticfiles /Shop/mediafiles
RUN chmod 755 /Shop/staticfiles /Shop/mediafiles

# Expose port
EXPOSE 8000

# CMD for development: migrate + runserver with auto-reload
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
