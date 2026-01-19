#!/bin/bash
set -e

echo "⏳ Waiting for database..."
until nc -z db 5432; do
  sleep 1
done

echo "✅ Database is up"

echo "🚀 Running migrations..."
alembic -c alembic.ini upgrade head

echo "🌱 Seeding database..."
python -m app.db.seed || echo "Seed skipped (already seeded)"

echo "🔥 Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000