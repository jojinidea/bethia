#!/bin/bash

# Play agent against specified program
# Example:
# ./playc.sh lookt 12345

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <player> <port> <num>" >&2
  exit 1
fi

for ((i = 1; i <= $3; i++)); do
    a=50005
    ./servt -p $(($a+$i)) & sleep 0.1
    ./agent -p $(($a+$i)) & sleep 0.1
    python3.7 agent.py -p $(($a+$i)) & sleep 0.1
    
done



