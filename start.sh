#!/usr/bin/env bash

# BIAI CRM Startup Script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "           🚀 Starting BIAI CRM System                     "
echo "=========================================================="

# 1. Stop any currently running instances
./stop.sh 2>/dev/null || true

# 2. Python Virtual Environment Check
if [ ! -d "backend/venv" ]; then
  echo "📦 Creating Python virtual environment..."
  python3 -m venv backend/venv
  backend/venv/bin/pip install --upgrade pip
  backend/venv/bin/pip install -r backend/requirements.txt
fi

# 3. Node Dependencies Check
if [ ! -d "frontend/node_modules" ]; then
  echo "📦 Installing Frontend dependencies..."
  (cd frontend && npm install)
fi

# 4. Database initialization if needed
if [ ! -f "crm.db" ]; then
  echo "🗄️ Initializing SQLite Database with 20 sample enquiries..."
  PYTHONPATH=backend backend/venv/bin/python backend/scripts/import_csv.py
fi

# 5. Start Backend Server (Detached process)
echo "⚡ Starting FastAPI Backend on port 8000..."
python3 -c "
import subprocess, sys
p = subprocess.Popen(
    [sys.argv[1], 'app.main:app', '--app-dir', sys.argv[2], '--host', '127.0.0.1', '--port', '8000', '--reload'],
    stdout=open('$DIR/backend.log', 'w'),
    stderr=subprocess.STDOUT,
    start_new_session=True
)
with open('$DIR/.backend.pid', 'w') as f:
    f.write(str(p.pid))
" "$DIR/backend/venv/bin/uvicorn" "$DIR/backend"

# 6. Start Frontend Server (Detached Node process)
echo "🎨 Starting Vite Frontend on port 5173..."
cd "$DIR/frontend"
node -e "
const fs = require('fs');
const { spawn } = require('child_process');
const out = fs.openSync('$DIR/frontend.log', 'w');
const p = spawn('./node_modules/.bin/vite', ['--host', '0.0.0.0', '--port', '5173'], {
    detached: true,
    stdio: ['ignore', out, out]
});
p.unref();
fs.writeFileSync('$DIR/.frontend.pid', String(p.pid));
"
cd "$DIR"

# 7. Wait for services to be ready
echo "⏳ Waiting for services to initialize..."
for i in {1..25}; do
  if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1 && curl -s http://127.0.0.1:5173 > /dev/null 2>&1; then
    echo "✅ Services are live!"
    break
  fi
  sleep 1
done

echo ""
echo "=========================================================="
echo "  🎉 BIAI CRM is ready and running!                       "
echo "=========================================================="
echo "  🌐 Frontend App:     http://localhost:5173              "
echo "  🔌 Backend API:      http://localhost:8000              "
echo "  📚 Swagger Docs:     http://localhost:8000/docs         "
echo "=========================================================="
echo "  🛑 To stop all servers, run: ./stop.sh                  "
echo "=========================================================="
