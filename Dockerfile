FROM python:3.12-slim

ARG DEV=false
ENV PYTHONBUFFERED 1

WORKDIR /nebustesting

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN if ["$DEV" == "true"]; then poetry install --with dev --no-root; else poetry install --only main --no-root; fi

COPY ./ ./

RUN chmod +x scripts/unicorn.sh