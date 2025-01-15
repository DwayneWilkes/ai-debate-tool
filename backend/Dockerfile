# Use an official Python image as a base
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /ai-debate-tool

# Copy the backend directory into /app
COPY backend /ai-debate-tool/backend

# Install dependencies from requirements.txt in /app/backend
RUN pip install --no-cache-dir -r /ai-debate-tool/backend/requirements.txt

# Expose the Flask port (5000)
EXPOSE 5000

# Set the default command to run your app
CMD ["python", "-m", "backend.app.main"]
