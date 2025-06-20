#!/bin/bash
# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
# Using the same MACHINE_IPS variable as other scripts
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

user="$DB_USER"

# Prompt for sudo password
read -s -p "Enter sudo password: " sudo_password
echo ""

# Loop through each machine to install ncdu
for machine in "${machines[@]}"; do
  echo "Starting ncdu install on $machine..."
  
  # Create a temporary script with the commands
  temp_script=$(mktemp)
  cat << 'REMOTE_SCRIPT' > "$temp_script"
    export DEBIAN_FRONTEND=noninteractive
    echo "$1" | sudo -S apt-get update > /dev/null 2>&1
    echo "$1" | sudo -S apt-get install -y ncdu
    if [ $? -eq 0 ]; then
      echo "Successfully installed ncdu on $(hostname)"
    else
      echo "Failed to install ncdu on $(hostname)"
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
  
  # Add a small delay between machines
  sleep 2
done

echo "NCDU installation process completed on all machines."
