# Base image for building
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY backend/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --target=/dependencies -r requirements.txt

# Final image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /ai-debate-tool

# Copy the dependencies
COPY --from=builder /dependencies /usr/local/lib/python3.11/site-packages

# Copy the rest of the app
COPY backend /ai-debate-tool/backend

# Expose the Flask port
EXPOSE 5000

# Add metadata
LABEL maintainer="dwayne.wilkes@gmail.com"
LABEL version="0.1"
LABEL description="AI Debate Tool Backend"

# Set the default command to run the app
CMD ["python", "-m", "backend.app.main"]
