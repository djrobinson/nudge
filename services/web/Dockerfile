FROM spark

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get -y install \
    libffi-dev \
    libssl-dev \
    python \
    python-dev \
    python-pip

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements
COPY ./project/requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY ./project /usr/src/app
