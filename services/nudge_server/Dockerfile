FROM python:3.7-slim

RUN apt-get update -y
RUN apt-get install -y gcc

# Create a user
RUN adduser --disabled-login quart
# Set working directory for the purpose of this Dockerfile
WORKDIR /home/quart

# Copy requirements to the app root
COPY requirements.txt ./requirements.txt
# Create a virtual environment and install the dependecies
RUN pip install --no-cache-dir -r requirements.txt --upgrade && \
  chown -R quart:quart ./

# Copy the app into our user root
COPY ./ /home/quart/
# Make our entrypoint executable
RUN chmod +x ./boot.sh

# Set the user
USER quart
# Set the entrypoint
ENTRYPOINT ["sh", "./boot.sh"]

# base image
FROM node:11.10.1

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY nudge_client/package.json /usr/src/app/package.json
RUN npm install
RUN npm install -g react-scripts

# start app
CMD ["npm", "start"]