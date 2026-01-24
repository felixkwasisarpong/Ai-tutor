#!/bin/sh
set -e

echo "Running migrations..."
if ! alembic upgrade head; then
  echo "Migration failed; stamping head to recover missing revisions..."
  python - <<'PY'
import os
import sys

from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("DATABASE_URL is not set; cannot reset alembic_version", file=sys.stderr)
    sys.exit(1)

config = Config("alembic.ini")
script = ScriptDirectory.from_config(config)
head = script.get_current_head()
if not head:
    print("No alembic head found; cannot reset alembic_version", file=sys.stderr)
    sys.exit(1)

engine = create_engine(db_url)
with engine.begin() as conn:
    conn.execute(
        text(
            "CREATE TABLE IF NOT EXISTS alembic_version ("
            "version_num VARCHAR(32) NOT NULL)"
        )
    )
    conn.execute(text("DELETE FROM alembic_version"))
    conn.execute(
        text("INSERT INTO alembic_version (version_num) VALUES (:v)"),
        {"v": head},
    )
print(f"Stamped alembic_version to {head}")
PY
  alembic upgrade head
fi

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
