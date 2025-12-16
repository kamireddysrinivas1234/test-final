#!/usr/bin/env sh
set -e

# wait for db if using postgres
if echo "$DATABASE_URL" | grep -q "postgresql"; then
  echo "Waiting for Postgres..."
  # basic wait loop
  python - <<'PY'
import os, time, socket, urllib.parse
url=os.environ.get("DATABASE_URL","")
u=urllib.parse.urlparse(url)
host=u.hostname or "db"
port=u.port or 5432
for i in range(60):
    try:
        s=socket.create_connection((host, port), timeout=2)
        s.close()
        print("Postgres is up")
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Postgres not reachable")
PY
fi

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
