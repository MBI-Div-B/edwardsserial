ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION
RUN pip install poetry 

RUN mkdir /code
WORKDIR /code
ADD pyproject.toml /code/
#RUN poetry config virtualenvs.create false --local && poetry run pip install --upgrade pip && poetry install --verbose
RUN poetry export -f requirements.txt --dev -o requirements.txt && pip install requirements.txt
