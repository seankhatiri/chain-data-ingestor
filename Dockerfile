# FROM python:3.8.12-slim@sha256:db43e371901603e59b49a078a82b0440432447f090ab124a6de5acc75a2b3d11 AS Base

# FROM Base AS Builder

# ARG DEPLOYMENT_ENVIRONMENT='test'

# ENV POETRY_VERSION=1.1.14 \
#     DEPLOYMENT_ENVIRONMENT=$DEPLOYMENT_ENVIRONMENT

# RUN mkdir /install

# WORKDIR /install

# RUN apt-get update && apt-get install -y g++ gcc libwebp-dev

# #RUN pip install "poetry==$POETRY_VERSION"

# #COPY poetry.lock pyproject.toml ./

# #RUN poetry config virtualenvs.create false && poetry install $(test "$DEPLOYMENT_ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

# COPY requirements.txt  /requirements.txt

# RUN pip install --prefix=/install -r /requirements.txt

# FROM Base AS RUN

# ENV FLASK_ENV development

# COPY --from=Builder /install /usr/local

# RUN python -m spacy download en_core_web_sm

# COPY . /app

# WORKDIR /app/mongo-python-driver-3.12.0

# RUN python setup.py install

# WORKDIR /app

# ADD data/models/transformers/all-MiniLM-L6-v2.tar.gz /app/data/models/transformers/

# RUN ls /app/data/models/transformers

# RUN pip3 install 'pymongo[srv]'

# RUN groupadd -r app && useradd --no-log-init -r -g app app

# ENV PYTHONPATH "${PYTHONPATH}:/app"

# ENTRYPOINT ["python3"]

# CMD ["main.py"]

FROM python:3.8

RUN apt-get update && apt-get install -y postgresql-client

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY init.sh ./

RUN chmod +x init.sh

EXPOSE 5001

CMD dockerize -wait tcp://db:5432 -timeout 60s ./init.sh
