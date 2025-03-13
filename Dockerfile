# Use a base image with Python pre-installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["/bin/sh", "-c", "python main.py < input.txt"]


