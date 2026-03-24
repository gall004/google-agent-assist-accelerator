#!/usr/bin/env bash
# ===========================================================================
# local-dev.sh — Start all services for local development
# ===========================================================================
set -euo pipefail

echo "🚀 Starting Google Agent Assist Accelerator (local development)..."

# Verify Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker is not running. Please start Docker and try again."
  exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
  echo "⚠️  No .env file found. Copying from .env.example..."
  cp .env.example .env
  echo "📝 Please edit .env with your GCP project values before proceeding."
  exit 1
fi

# Start all services
docker compose up --build "$@"
