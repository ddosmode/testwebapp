#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-prod}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Running database migrations in mode: $MODE"

cd "$PROJECT_ROOT"

if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Copy .env.example to .env and fill in the values."
    exit 1
fi

if [ "$MODE" = "prod" ]; then
    COMPOSE_FILES="-f docker-compose.yml -f docker-compose.prod.yml"
else
    COMPOSE_FILES=""
fi

docker compose $COMPOSE_FILES run --rm backend alembic upgrade head

echo "Migrations complete!"
