FROM python:3.7-slim

RUN apt-get update -y
RUN apt-get install -y gcc

# Create a user
RUN adduser --disabled-login quart
# Set working directory for the purpose of this Dockerfile
WORKDIR /usr/src/server

# Copy requirements to the app root
COPY requirements.txt ./requirements.txt
# Create a virtual environment and install the dependecies
RUN pip install --no-cache-dir -r requirements.txt --upgrade

# Copy the app into our user root
COPY ./ /usr/src/server
# Make our entrypoint executable
RUN chmod +x ./boot.sh

# Set the entrypoint
ENTRYPOINT ["sh", "./boot.sh"]