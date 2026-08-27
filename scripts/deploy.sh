#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-prod}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Deploying TestWebApp in mode: $MODE"
echo "Project root: $PROJECT_ROOT"

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

echo "Building services..."
docker compose $COMPOSE_FILES build

echo "Applying database migrations..."
docker compose $COMPOSE_FILES run --rm backend alembic upgrade head

echo "Starting services..."
docker compose $COMPOSE_FILES up -d

echo "Waiting for services to be healthy..."
sleep 10

echo "Service status:"
docker compose $COMPOSE_FILES ps

echo "Deployment complete!"
