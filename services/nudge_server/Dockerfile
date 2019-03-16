# base image
FROM node:11.10.1

# set working directory
RUN mkdir /usr/src/nudge_client
WORKDIR /usr/src/nudge_client

# add `/usr/src/client/node_modules/.bin` to $PATH
ENV PATH /usr/src/nudge_client/node_modules/.bin:$PATH

# install and cache client dependencies
COPY nudge_client /usr/src/nudge_client
RUN npm install
RUN npm install -g react-scripts

RUN npm run build

# start app
FROM python:3.7-slim

RUN apt-get update -y
RUN apt-get install -y gcc

# Create a user
RUN adduser --disabled-login quart
# Set working directory for the purpose of this Dockerfile
WORKDIR /usr/src

# Copy requirements to the app root
COPY requirements.txt ./requirements.txt
# Create a virtual environment and install the dependecies
RUN pip install --no-cache-dir -r requirements.txt --upgrade && \
  chown -R quart:quart ./

# Copy the app into our user root
COPY ./ /usr/src
# Make our entrypoint executable
RUN chmod +x ./boot.sh

# Set the user
USER quart
# Set the entrypoint
ENTRYPOINT ["sh", "./boot.sh"]