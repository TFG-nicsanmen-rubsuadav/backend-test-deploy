# Base image
FROM python:3.10-alpine

# Working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create local_settings.py and set environment variables
RUN echo "GOOGLE_APPLICATION_CREDENTIALS_BASE64 = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_BASE64')" >> local_settings.py
RUN echo "FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')" >> local_settings.py
RUN echo "FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')" >> local_settings.py
RUN echo "FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')" >> local_settings.py
RUN echo "FIREBASE_STORAGE_BUCKET = os.getenv('FIREBASE_STORAGE_BUCKET')" >> local_settings.py
RUN echo "FIREBASE_MESSAGING_SENDER_ID = os.getenv('FIREBASE_MESSAGING_SENDER_ID')" >> local_settings.py
RUN echo "FIREBASE_APP_ID = os.getenv('FIREBASE_APP_ID')" >> local_settings.py

# Copy the rest of the project files
COPY . .

# Expose the server port
EXPOSE 8000

# Command to start the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]