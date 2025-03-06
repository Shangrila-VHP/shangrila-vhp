#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# List of machines (replace with actual IP addresses)
machines=("10.0.0.226" "10.0.0.124" "10.0.0.111" "10.0.0.108")
user="$DB_USER"
ssh_key_passphrase="your_ssh_key_passphrase"

# Loop through each machine to install chrony and set the time to EST
for machine in "${machines[@]}"; do
  sshpass -p "$ssh_key_passphrase" ssh -o StrictHostKeyChecking=no -t "$user@$machine" << EOF
    sudo apt-get update
    sudo apt-get install -y chrony
    sudo timedatectl set-timezone America/New_York
    sudo systemctl restart chrony
    echo "Chrony installed and time set to EST on $machine"
EOF
done

echo "Chrony installation and time setting complete on all machines."
