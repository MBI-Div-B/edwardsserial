ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION
RUN pip install poetry

RUN mkdir /code
WORKDIR /code
ADD pyproject.toml /code/
RUN poetry run pip install --upgrade pip && poetry install --verbose

