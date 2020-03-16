ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION


RUN mkdir /code
WORKDIR /code
ADD pyproject.toml /code/

RUN pip install poetry

RUN poetry run pip install --upgrade pip && poetry install

