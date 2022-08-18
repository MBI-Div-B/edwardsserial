ARG PYTHON_VERSION=3.8

FROM python:$PYTHON_VERSION as python
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

FROM python as poetry
ARG POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
ARG POETRY_VERSION=1.1.14
RUN curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /code/
RUN poetry lock
RUN poetry install --no-interaction --no-ansi --no-root -vvv

# ------old ---------

#ENV BUILD_PACKAGES pandoc rsync openssh-client build-essential
## Disable automatic cache cleanup
#RUN rm /etc/apt/apt.conf.d/docker-clean
#
## This volume is discarded after the build process.
## It just reduces the image size without deleting the directory.
#VOLUME ["/root/.cache/pypoetry"]
#VOLUME ["/var/cache/apt"]
#
#RUN mkdir /code
#WORKDIR /code
#
#RUN apt-get update -y && apt-get install -y $BUILD_PACKAGES
#RUN pip install poetry && poetry config virtualenvs.create true
#
#
#COPY pyproject.toml poetry.lock /code/
#RUN poetry lock
#RUN poetry install -vvv --no-interaction
CMD bash
