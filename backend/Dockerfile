FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root

ENV PYTHONPATH=/app

COPY ./scripts /app/scripts

COPY ./alembic.ini /app/

COPY ./app /app/app


CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
