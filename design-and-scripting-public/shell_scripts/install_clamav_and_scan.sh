#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# List of machines (replace with actual IP addresses)
machines=("10.0.0.226" "10.0.0.124" "10.0.0.111" "10.0.0.108")
user="$DB_USER"
ssh_key_passphrase="your_ssh_key_passphrase"

# Loop through each machine to install ClamAV, update definitions, and run a scan
for i in "${!machines[@]}"; do
  machine="${machines[$i]}"
  delay=$((i * 2700))  # 2700 seconds = 45 minutes

  echo "Starting ClamAV installation and scan on $machine with a delay of $delay seconds..."
  
  sshpass -p "$ssh_key_passphrase" ssh -o StrictHostKeyChecking=no -t "$user@$machine" "(
    hostname=\$(uname -n)
    echo 'Hostname: \$hostname'
    echo 'Killing any existing ClamAV scans...'
    sudo pkill clamscan || true
    sudo pkill freshclam || true

    echo 'Updating package list...'
    sudo apt-get update &&
    echo 'Installing ClamAV...'
    sudo apt-get install -y clamav clamav-daemon &&
    echo 'Waiting for ClamAV installation to complete...'
    sleep 120 &&  # Wait time to ensure the installation completes
    echo 'Updating ClamAV definitions...'
    sudo freshclam &&
    sudo systemctl start clamav-freshclam &&
    echo 'Waiting for $delay seconds before starting the scan on $machine (\$hostname)...'
    sleep $delay &&
    echo 'Starting ClamAV scan on \$hostname...'
    # Run clamscan with lower priority and limited CPU usage
    if [ \$(nproc) -ge 8 ]; then
      sudo taskset -c 0-3 nice -n 10 clamscan -r --remove /
    else
      sudo nice -n 10 clamscan -r --remove /
    fi &&
    echo 'ClamAV installed, definitions updated, and scan completed on $machine (\$hostname)'
  ) &"  # Run the commands in the background
done

echo "ClamAV installation, update, and scan initiated on all machines."
