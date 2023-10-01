##################################################
# build image
##################################################
FROM python:3.11-slim-bookworm  as builder
RUN apt-get update && \
  apt-get install -y libmariadb-dev gcc default-mysql-client build-essential vim gettext

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /src

##################################################
# local image
##################################################
FROM builder as local

COPY ./src/requirements /src/requirements
RUN pip install --upgrade pip && \
  pip install --no-cache-dir --upgrade -r requirements/base.txt

COPY ./src /src

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]

##################################################
# debug image
##################################################
FROM local as debug

CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]