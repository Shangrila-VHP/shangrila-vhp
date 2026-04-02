#!/bin/bash
# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
# Using the same MACHINE_IPS variable from the gather_machine_info script
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

user="$DB_USER"

# Loop through each machine to install chrony and set the time to EST
for machine in "${machines[@]}"; do
  echo "Installing chrony and setting time on: $machine"
  
  # Using SSH directly without sshpass for better security
  # This will use your SSH key and prompt for the passphrase if needed
  ssh -o StrictHostKeyChecking=no -t "$user@$machine" << EOF
    sudo apt-get update
    sudo apt-get install -y chrony
    sudo timedatectl set-timezone America/New_York
    sudo systemctl restart chrony
    echo "Chrony installed and time set to EST on $machine"
EOF

  # Add a small delay between machines
  sleep 2
done

echo "Chrony installation and time setting complete on all machines."
