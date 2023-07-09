# Build: docker build -t grocery-list-api .
# alpine is the image used by linux that is lightweight and stripped back
FROM python:3.9.16-alpine3.17
# i am the mainteaner of this image
LABEL maintainter='nicolascope'
# tell python to not buffer the outputs, prevents delays in logs
ENV PYTHONUNBUFFERED 1
# copy the requirements.txt file from the local machine to the docker image
COPY ./requirements.txt /tmp/requirements.txt
# copy the requirements.dev.txt file from the local machine to the docker image when running in development
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# copy app directory from local machine to docker image
COPY ./app /app
# define the working directory where commands will be run
WORKDIR /app
# access the port 8000
EXPOSE 8000
# set the default dev arg to false and overide it when running in development in docer-compose.yml
ARG DEV=false
# run a command on the image. only run command to only create one image layer.
# creates a new virtual environment
# upgrade pip and install requirements
# remove the temporary directory keeps docker image lightweight
# create a users to run the application best practice not to use the root users.
# if the dev arg is true install the dev requirements
# the apk installs the postgresql client and the .tmp-build-deps installs the build dependencies
# the --virtual flag creates a virtual package that can be removed later
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-users
# adds python to the path
ENV PATH="/py/bin:$PATH"
# switch to the django-users. up till now the commands have been run as root users.
USER django-user