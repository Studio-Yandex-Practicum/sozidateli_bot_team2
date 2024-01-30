FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/* \
    && pip install gunicorn \
    && pip install -r requirements.txt --no-cache-dir

COPY app ./app
COPY src ./src
COPY alembic.ini alembic.ini
COPY alembic ./alembic
COPY --chmod=0755 scripts/create_migrations.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/create_migrations.sh"]

CMD gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
