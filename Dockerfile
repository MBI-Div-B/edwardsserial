ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install poetry && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock /code/
RUN poetry install -vvv --no-interaction
