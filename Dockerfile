# Base image
FROM python:3.10

# Working directory
WORKDIR /Shop

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt /Shop/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Create and set permissions for staticfiles folder
RUN mkdir -p /Shop/staticfiles
RUN chmod 755 /Shop/staticfiles

# Copy project files
COPY . /Shop/

# Collect static files
RUN python manage.py collectstatic --noinput

# Django settings
ENV DJANGO_SETTINGS_MODULE=config.settings

# Expose port
EXPOSE 8000

# Run migrations and start Daphne server
CMD ["sh", "-c", "python manage.py migrate"]
#CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 einvestment.asgi:application"]

