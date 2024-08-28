
#
# AUTHOR: William A. Morris
# CREATION_DATE: 2024-08-28
# PURPOSE:
#   create Docker Container from generated application artifacts
#

# Container will be run on x86-64 Linux Platform
# Pull python 3.12
FROM --platform=x86-64 python:3.12-alpine

# ENV SYS_VAR=default_value

# create and move to directory /app to store artifacts
WORKDIR /app

# copy Java ARchieve (Jar) into /app folder
COPY lib/* .

# run dep
RUN pip install gunicorn

# set entrypoint (command which will run when container is started)
ENTRYPOINT gunicorn --chdir /app app.wsgi

# expose appropriate API port
EXPOSE 8080
