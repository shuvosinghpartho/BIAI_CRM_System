#!/usr/bin/env bash

# BIAI CRM Shutdown Script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Stopping BIAI CRM services..."

# Kill by PID files if exist
if [ -f "$DIR/.backend.pid" ]; then
  kill -9 "$(cat "$DIR/.backend.pid")" 2>/dev/null || true
  rm -f "$DIR/.backend.pid"
fi

if [ -f "$DIR/.frontend.pid" ]; then
  kill -9 "$(cat "$DIR/.frontend.pid")" 2>/dev/null || true
  rm -f "$DIR/.frontend.pid"
fi

# Fallback: kill anything listening on ports 8000 and 5173
lsof -ti :8000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti :5173 2>/dev/null | xargs kill -9 2>/dev/null || true

echo "All BIAI CRM services have been stopped."
