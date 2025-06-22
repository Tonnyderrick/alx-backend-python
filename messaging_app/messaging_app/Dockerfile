# Dockerfile

# Use official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire app into the container
COPY . .

# Expose the default Django port
EXPOSE 8000

# Run Django development server with explicit -p in CMD
CMD ["python", "manage.py", "runserver", "-p", "8000", "0.0.0.0:8000"]
