#!/bin/bash

# List of machines
machines=("class01" "class02" "class03" "class04")

# Loop over each machine and run the command
for machine in "${machines[@]}"; do
    cat ./ollama_script.sh | ssh "$machine" /bin/bash &
done

# Wait for all background processes to finish
wait
