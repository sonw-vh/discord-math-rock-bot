FROM python:3.8-slim-buster

# Install the required packages
RUN pip install discord.py google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Copy the bot files into the image
COPY main.py /app/

# Run the bot when the container starts
CMD ["python", "/app/main.py"]
