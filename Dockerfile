ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION
RUN pip install poetry 

RUN mkdir /code
WORKDIR /code
ADD pyproject.toml /code/
RUN poetry config virtualenvs.in-project true && poetry run pip install --upgrade pip && poetry install --verbose

