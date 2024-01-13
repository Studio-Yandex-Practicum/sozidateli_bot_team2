FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install gunicorn
RUN pip install -r requirements.txt --no-cache-dir

COPY ./src ./src
COPY --chmod=0755 scripts/create_migrations.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/create_migrations.sh"]

CMD gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8080
