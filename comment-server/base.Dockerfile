FROM python:3.9.2-alpine

# upgrade pip
RUN pip install --upgrade pip
RUN pip install --upgrade poetry

# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot
# copy all the files to the container
COPY --chown=nonroot:nonroot pyproject.toml .
# python setup
RUN poetry install
