# Use Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv

# Upgrade awscli
RUN python -m pip install --upgrade awscli

# Set environment variables
ENV VIRTUAL_ENV="/opt/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements file
COPY requirements.txt .

# Install required packages
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Upgrade pip to the latest version
RUN /opt/venv/bin/pip install --upgrade pip

# Install Gunicorn
RUN /opt/venv/bin/pip install gunicorn

# Copy application files
COPY . .

# Command to run the application with Gunicorn
CMD ["/opt/venv/bin/gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]
