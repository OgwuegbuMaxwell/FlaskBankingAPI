# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app



# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with an increased timeout
RUN pip install --default-timeout=1200 --no-cache-dir -r requirements.txt


# Copy the rest of the application
COPY . .

CMD ["python", "app.py"]
