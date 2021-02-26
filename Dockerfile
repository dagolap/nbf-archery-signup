FROM python:3.9.2

WORKDIR /app

# Env setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME=/poetry \
    POETRY_VERSION=1.1.4

COPY . ./

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry install

WORKDIR /app/archerysignup

ENTRYPOINT ["/bin/bash", "/app/archerysignup/entrypoint.sh"]



# Install dependencies
