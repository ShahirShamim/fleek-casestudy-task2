FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY webapp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the webapp code
COPY webapp /app/webapp
# Copy the test_emails directory into the container
COPY test_emails /app/test_emails

# Set environment variable for the app to find the test_emails
ENV TEST_EMAILS_DIR=/app/test_emails

EXPOSE 5000

# Run gunicorn serving the flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "/app/webapp", "app:app"]
