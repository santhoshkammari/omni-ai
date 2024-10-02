#!/bin/bash

# Function to kill processes using a specific port
kill_process_on_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        echo "Killing process on port $port (PID: $pid)"
        kill -9 $pid
    fi
}

# Kill any process using port 3000 (React default port)
kill_process_on_port 3000

# Kill any process using port 8888 (Your backend port)
kill_process_on_port 8888

# Start the backend
cd ~/MAIN/omni-ai/src/main/backend
python main.py &
BACKEND_PID=$!

# Wait for the backend to start (adjust sleep time as needed)
sleep 5

# Start the frontend
cd ~/MAIN/omni-ai/src/main/frontend
npm start &
FRONTEND_PID=$!

# Save PIDs to a file for easy killing later
echo $BACKEND_PID > ~/MAIN/omni-ai/running_pids.txt
echo $FRONTEND_PID >> ~/MAIN/omni-ai/running_pids.txt

echo "Backend and Frontend started. PIDs saved in ~/MAIN/omni-ai/running_pids.txt"