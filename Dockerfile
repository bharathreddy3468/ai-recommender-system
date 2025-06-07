# Use a lightweight base Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy all necessary files
COPY main.py database.py app.py requirements.txt ./
COPY src/ ./src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port if running a web app (like Flask)
EXPOSE 8080

# Command to run the app
CMD ["python", "main.py"]
