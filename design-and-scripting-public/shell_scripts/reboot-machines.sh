#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

# Environment variables
user="$DB_USER"
SSH_OPTS="-o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 -t"

# Loop through each machine to reboot
for machine in "${machines[@]}"; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Rebooting $machine in 30 seconds..."

    # Execute reboot on each machine with a 30-second delay
    ssh ${SSH_OPTS} "$user@$machine" "
        hostname=\$(uname -n)
        echo '[$(date '+%Y-%m-%d %H:%M:%S')] Hostname: \$hostname'
        echo 'Rebooting \$hostname...'
        
        # Delay for 30 seconds before reboot
        sleep 30
        
        # Reboot the machine
        sudo reboot
    " &
done

# Wait for all background processes (reboots) to finish before the script exits
wait

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Reboot initiated on all machines."

