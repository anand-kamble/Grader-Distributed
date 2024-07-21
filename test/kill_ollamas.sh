#!/bin/bash

# List of machines
machines=("class01" "class02" "class03" "class04" "class05" "class06" "class07" "class08" "class09" "class10" "class11" "class12" "class13" "class14" "class15" "class16" "class17" "class18" "class19")

# Get the current machine's hostname
current_machine=$(hostname)

# Function to kill the process on a remote machine
kill_process_on_machine() {
    local machine=$1
    echo "Killing process on machine: $machine"
    ssh -o "StrictHostKeyChecking no" "$machine" "bash -s" << 'EOF'
port=11434
pid=$(lsof -i :$port -t)
if [ -n "$pid" ]; then
    echo "Killing process with PID $pid using port $port"
    kill -9 $pid
    echo "Process killed."
else
    echo "No process found using port $port."
fi
EOF
}

# Loop over each machine and kill the process in the background
for machine in "${machines[@]}"; do
    if [ "$machine" != "$current_machine" ]; then
        kill_process_on_machine "$machine" &
    fi
done

# Wait for all background processes to finish
wait
