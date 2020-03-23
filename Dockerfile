ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION
RUN pip install poetry

RUN mkdir /code
WORKDIR /code
COPY pyproject.toml /code/
RUN poetry config virtualenvs.create false
RUN poetry install -vvv --no-interaction

