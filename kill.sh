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

# Read PIDs from the file if it exists
if [ -f ~/MAIN/omni-ai/running_pids.txt ]; then
    PIDS=$(cat ~/MAIN/omni-ai/running_pids.txt)

    # Kill processes
    for PID in $PIDS
    do
        if ps -p $PID > /dev/null
        then
            kill $PID
            echo "Killed process $PID"
        fi
    done

    # Remove the PID file
    rm ~/MAIN/omni-ai/running_pids.txt
fi

# Kill any remaining node processes related to the project
pkill -f "node.*omni-ai/src/main/frontend"

echo "Backend and Frontend stopped."