FROM python:3.8-slim-bullseye
WORKDIR /app
EXPOSE 5000

RUN apt-get update; apt-get install -y  git apt-utils iputils-ping 1>/dev/null

RUN pip install --upgrade pip

WORKDIR /app
RUN pip install pipenv gunicorn
RUN pip install pipenv uvicorn
COPY ./Pipfile* ./
RUN pipenv install --deploy --system
COPY . .

USER 1001
CMD gunicorn -b "0.0.0.0:5000" src.app:api -w 4 -k uvicorn.workers.UvicornWorker --reload --timeout 666 --log-level=debug 2>&1 | tee -a /tmp/log