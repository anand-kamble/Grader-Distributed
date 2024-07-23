#!/bin/bash

# List of machines (IP addresses or hostnames)
MACHINES=(
    "class01" "class02" "class03" "class04" "class05"
    "class06" "class07" "class08" "class09" "class10"
    "class11" "class12" "class13" "class14" "class15"
    "class16" "class17" "class18" "class19"
)

# SSH user
USER="amk23j"

# Function to check GPU status on a single machine
check_gpu() {
  local machine=$1
  local output=$(ssh -o ConnectTimeout=5 $USER@$machine "nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,utilization.memory --format=csv,noheader,nounits" 2>/dev/null)
  if [ $? -ne 0 ]; then
    echo "$machine,Failed to connect"
  else
    echo "$output" | while IFS=, read -r name temp util_gpu util_mem; do
      echo "$machine,$name,$temp,$util_gpu,$util_mem"
    done
  fi
}

# Function to monitor GPUs on all machines
monitor_gpus() {
  clear
  while true; do
    echo "Machine,Name,Temp (C),GPU Util (%),Mem Util (%)"
    for machine in "${MACHINES[@]}"; do
      check_gpu $machine
    done
    sleep 0.01
    clear
  done
}

# Start monitoring
monitor_gpus
