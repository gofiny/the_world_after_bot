# syntax=docker/dockerfile:experimental

FROM python:3.11.0-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PDM_VERSION=2.4.0 \
    PYTHONPATH=/opt/app/__pypackages__/3.11/lib

RUN pip install "pdm==$PDM_VERSION" && \
    pdm config venv.in_project false && \
    pdm config check_update false && \
    pdm config python.use_venv false

WORKDIR /opt/app

COPY pyproject.toml pdm.lock README.md /opt/app/

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

COPY . .

CMD ["pdm", "run", "start"]
