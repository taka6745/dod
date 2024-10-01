# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables for non-interactive installs and better control over buffer handling
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies (optional: add any required OS-level packages here)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the application port to the outside world
EXPOSE 8000

# Define environment variables for MySQL connection pointing to the host's localhost
ENV MYSQL_HOST=localhost \
    MYSQL_PORT=3306 \
    MYSQL_USER=user \
    MYSQL_PASSWORD=password \
    MYSQL_DB=dbname

# Run the FastAPI application with Uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
