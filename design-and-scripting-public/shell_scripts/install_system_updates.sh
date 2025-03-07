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

# Loop through each machine to perform updates
for machine in "${machines[@]}"; do
  echo "Starting system update on $machine..."
  
  # Create a temporary script with the commands
  temp_script=$(mktemp)
  cat << 'REMOTE_SCRIPT' > "$temp_script"
    export DEBIAN_FRONTEND=noninteractive
    echo "$1" | sudo -S apt-get update > /dev/null 2>&1
    echo "$1" | sudo -S apt-get upgrade -y
    echo "$1" | sudo -S apt-get autoremove -y
    echo "$1" | sudo -S apt-get autoclean -y
    if [ $? -eq 0 ]; then
      echo "Successfully updated system on $(hostname)"
    else
      echo "Failed to update system on $(hostname)"
      exit 1
    fi
REMOTE_SCRIPT

  # Execute the remote script
  ssh -o StrictHostKeyChecking=no "$user@$machine" "bash -s" -- "$sudo_password" < "$temp_script"
  
  # Clean up
  rm "$temp_script"
  if [ $? -ne 0 ]; then
    echo "Failed to complete updates on $machine"
  fi
  
  # Add a small delay between machines
  sleep 2
done

echo "System update process completed on all machines."
