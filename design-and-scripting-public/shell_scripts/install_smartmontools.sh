#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# List of machines
machines=("10.0.0.226" "10.0.0.124" "10.0.0.111" "10.0.0.108")
user="$DB_USER"

# Prompt for sudo password
read -s -p "Enter sudo password: " sudo_password
echo ""

# Loop through each machine to install the given apt package 
for machine in "${machines[@]}"; do
  echo "Starting ncdu install on $machine..."
  
  # Create a temporary script with the commands
  temp_script=$(mktemp)
  cat << 'REMOTE_SCRIPT' > "$temp_script"
    export DEBIAN_FRONTEND=noninteractive
    echo "$1" | sudo -S apt-get update > /dev/null 2>&1
    echo "$1" | sudo -S apt-get install -y smartmontools 
    if [ $? -eq 0 ]; then
      echo "Successfully installed your package on $(hostname)"
    else
      echo "Failed to install your package on $(hostname)"
      exit 1
    fi
REMOTE_SCRIPT

  # Execute the remote script
  ssh -o StrictHostKeyChecking=no "$user@$machine" "bash -s" -- "$sudo_password" < "$temp_script"
  
  # Clean up
  rm "$temp_script"

  if [ $? -ne 0 ]; then
    echo "Failed to complete installation on $machine"
  fi
done

echo "installation process completed."
