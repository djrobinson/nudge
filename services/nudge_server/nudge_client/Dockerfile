# base image
FROM node:11.10.1

# set working directory
RUN mkdir /usr/src/client
WORKDIR /usr/src/client

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/client/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/client/package.json
RUN npm install
RUN npm install -g react-scripts

# start app
CMD ["npm", "start"]