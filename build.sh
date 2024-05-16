#!/bin/bash

# Function to find and kill processes using a given port
kill_process_using_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo "Killing process running on port $port"
        kill -9 $pid
    fi
}

# Kill processes using ports 5173 and 8000
kill_process_using_port 5173
kill_process_using_port 8000

# Remove all stopped containers, unused networks, dangling images, and build cache
docker system prune -f

# Build Docker images without cache
docker-compose build --no-cache

# Start Docker containers in detached mode
docker-compose up -d

# Start frontend (Vue.js)
echo "Starting frontend"
cd frontend/
npm install
npm run dev -- --port 5173 &

# Start backend (Python - Flask)
echo "Starting backend"
cd ../backend/
pip install -r requirements.txt
gunicorn app:app -b 127.0.0.1:8000 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
