#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

# Set up variables
user="$DB_USER"
info_dir="$HOME/documents/scripts/machine_info_audit"
audit_dir="$HOME/documents/scripts/machine_info_audit"
log_file="$HOME/documents/scripts/audit_log_$(date +'%Y-%m-%d_%H-%M-%S').log"

# Get the current timestamp
timestamp=$(date +'%Y-%m-%d_%H-%M-%S')

# Loop through each machine and check for changes
for machine in "${machines[@]}"; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting audit for $machine" >> "$log_file"
    
    latest_info_dir=$(ls -td "$info_dir"/*/ | head -n 1)
    current_info_file="$latest_info_dir/$machine-info.txt"
    previous_info_file="$audit_dir/$machine-info-prev.txt"
    diff_file="$audit_dir/$machine-info-diff_$timestamp.txt"
    
    # Compare current info with previous info if it exists
    if [ -f "$previous_info_file" ]; then
        diff "$previous_info_file" "$current_info_file" > "$diff_file"
        if [ -s "$diff_file" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Changes detected for machine $machine. See $diff_file for details." >> "$log_file"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes detected for machine $machine." >> "$log_file"
            rm "$diff_file"
        fi
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] No previous info found for machine $machine. Saving current info." >> "$log_file"
    fi

    # Save current info as previous info for future comparisons
    cp "$current_info_file" "$previous_info_file"
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Periodic audit complete. Check the log file at $log_file for details."
