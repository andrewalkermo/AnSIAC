FROM python:latest

WORKDIR /app

RUN python3 -m pip install poetry==1.5.0
RUN poetry config virtualenvs.create false

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN poetry install

COPY . /app

ENV PYTHONPATH="$PYTHONPATH:/app"

ENTRYPOINT [ "poetry", "run", "python3", "main.py" ]