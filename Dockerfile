# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the application file
COPY hello_world.py .

# Expose port 5010
EXPOSE 5010

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "hello_world.py"]
