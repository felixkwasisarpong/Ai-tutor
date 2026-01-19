FROM python:3.11-slim

WORKDIR /app

# System deps (needed for psycopg2, netcat)
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app + alembic + scripts
COPY app app
COPY alembic alembic
COPY alembic.ini alembic.ini
COPY scripts/start.sh /start.sh

RUN chmod +x /start.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["/start.sh"]