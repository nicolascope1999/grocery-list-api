# Build: docker build -t grocery-list-api .
# alpine is the image used by linux that is lightweight and stripped back
FROM python:3.9.16-alpine3.17
# i am the mainteaner of this image
LABEL maintainter='nicolascope'
# tell python to not buffer the outputs, prevents delays in logs
ENV PYTHONUNBUFFERED 1
# copy the requirements.txt file from the local machine to the docker image
COPY ./requirements.txt /tmp/requirements.txt
# copy app directory from local machine to docker image
COPY ./app /app
# define the working directory where commands will be run
WORKDIR /app
# access the port 8000
EXPOSE 8000
# run a command on the image. only run command to only create one image layer.
# creates a new virtual environment
# upgrade pip and install requirements
# remove the temporary directory keeps docker image lightweight
# create a user to run the application best practice not to use the root user.
RUN python -m venv /py && \
    pip install --upgrade && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user \
# adds python to the path
ENV PATH='/py/bin:$PATH'
# switch to the django-user. up till now the commands have been run as root user.
USER django-user