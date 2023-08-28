# Using lightweight alpine image
FROM python:3.11.4-alpine3.18

RUN apk add mysql mysql-client gcc musl-dev mariadb-connector-c-dev

# Installing packages
RUN apk update

RUN pip install --no-cache-dir pipenv

# Defining working diectory and adding source code
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY src ./src

# Install API dependencies
RUN pipenv install --system --deploy

#Start app
EXPOSE 500

ENTRYPOINT ["/usr/src/app/bootstrap.sh"]
