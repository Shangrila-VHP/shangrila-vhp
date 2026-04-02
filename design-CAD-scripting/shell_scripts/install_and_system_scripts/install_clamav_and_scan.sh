#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

# Environment variables
user="$DB_USER"
SSH_OPTS="-o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 -t"

# Loop through each machine to install ClamAV, update definitions, and run a scan
for i in "${!machines[@]}"; do
    machine="${machines[$i]}"
    delay=$((i * 2700))  # 2700 seconds = 45 minutes

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting ClamAV installation and scan on $machine with a delay of $delay seconds..."
    
    ssh ${SSH_OPTS} "$user@$machine" "(
        hostname=\$(uname -n)
        echo '[$(date '+%Y-%m-%d %H:%M:%S')] Hostname: \$hostname'
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
        echo '[$(date '+%Y-%m-%d %H:%M:%S')] Starting ClamAV scan on \$hostname...'
        # Run clamscan with lower priority and limited CPU usage
        if [ \$(nproc) -ge 8 ]; then
            sudo taskset -c 0-3 nice -n 10 clamscan -r --remove /
        else
            sudo nice -n 10 clamscan -r --remove /
        fi &&
        echo '[$(date '+%Y-%m-%d %H:%M:%S')] ClamAV installed, definitions updated, and scan completed on $machine (\$hostname)'
    ) &"  # Run the commands in the background
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ClamAV installation, update, and scan initiated on all machines."
