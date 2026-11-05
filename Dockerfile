FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY pyproject.toml README.md LICENSE NOTICE ./
COPY src ./src

RUN python -m pip install --no-cache-dir --upgrade pip build && \
    python -m pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    OEI_API_HOST=0.0.0.0 \
    OEI_API_PORT=8000 \
    OEI_DATA_DIR=/app/data \
    OEI_EXPORT_DIR=/app/exports

RUN groupadd --system --gid 1001 oei && \
    useradd --system --uid 1001 --gid oei --create-home --home-dir /home/oei oei

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY examples ./examples
COPY docs ./docs

RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels oei-core && \
    rm -rf /wheels && \
    mkdir -p /app/exports /app/data && \
    chown -R oei:oei /app

USER oei

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/v1/health', timeout=2).status == 200 else 1)"

CMD ["uvicorn", "oei.api.app:app", "--host", "0.0.0.0", "--port", "8000"]