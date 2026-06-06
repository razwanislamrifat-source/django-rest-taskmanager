FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/django/.local/bin:$PATH \
    DJANGO_SETTINGS_MODULE=taskmanager.settings

RUN useradd -m -u 1000 django

WORKDIR /app

COPY --from=builder /root/.local /home/django/.local
COPY --chown=django:django app/ .

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/auth/token/')" || exit 1

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--worker-tmp-dir", "/dev/shm", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "taskmanager.wsgi:application"]
