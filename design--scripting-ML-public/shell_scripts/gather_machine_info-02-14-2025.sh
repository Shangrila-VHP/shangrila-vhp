#!/bin/bash
# Source environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

user="$DB_USER"  # username from .env 

# Create the output directory using dynamic home directory
mkdir -p "$HOME/documents/scripts/machine_info_audit"

# Get the current timestamp
timestamp=$(date +'%Y-%m-%d_%H-%M-%S')

# Directory to save the output
output_dir="$HOME/documents/scripts/machine_info_audit/$timestamp"
audit_dir="$HOME/documents/scripts/machine_info_audit"
mkdir -p "$output_dir"
mkdir -p "$audit_dir"

# Loop through each machine and gather information
for machine in "${machines[@]}"; do
  echo "Processing machine: $machine"
  current_info_file="$output_dir/$machine-info.txt"
  previous_info_file="$audit_dir/$machine-info-prev.txt"
  backup_info_file="$audit_dir/$machine-info-prev_$timestamp.txt"
  diff_file="$audit_dir/$machine-info-diff_$timestamp.txt"
  
  echo "Connecting to $machine to gather information..."
  echo "Please enter your SSH passphrase when prompted..."
  sleep 2  # Give user time to read the message
  
  # Removed -t flag and modified the SSH command
  ssh -o StrictHostKeyChecking=no "$user@$machine" "bash -s" << 'EOF' > "$current_info_file"
    echo "Machine: $machine"
    echo "===================="
    echo "Timestamp: $(date +'%Y-%m-%d_%H-%M-%S')"
    echo "Hostname:"
    hostname
    echo
    echo "IP Address:"
    ip a | grep -i 'inet 10.0.0.'
    echo
    echo "Kernel Version:"
    uname -r
    echo
    echo "LXD Version:"
    lxd --version
    echo
    echo "CPU Info:"
    lscpu
    echo
    echo "Memory Info:"
    free -h
    echo
    echo "Disk Info:"
    lsblk
    echo
    echo "Disk Usage:"
    df -h
    echo
    echo "Network Interfaces:"
    ip link show
    echo
    echo "Network Configuration:"
    ip -d link show
    echo
    echo "Storage Pools:"
    lxc storage list
    echo
    echo "Detailed Storage Information:"
    echo "============================"
    echo "1. Physical Disks (including size):"
    lsblk -b -o NAME,SIZE,TYPE,MOUNTPOINT | grep "disk"
    echo
    echo "2. Partition Information:"
    lsblk -b -o NAME,SIZE,TYPE,MOUNTPOINT | grep "part"
    echo
    echo "3. LVM Information (if available without sudo):"
    which lvs && {
      echo "LVM Volumes:"
      lvs 2>/dev/null || echo "Requires elevated privileges"
      echo "Volume Groups:"
      vgs 2>/dev/null || echo "Requires elevated privileges"
      echo "Physical Volumes:"
      pvs 2>/dev/null || echo "Requires elevated privileges"
    } || echo "LVM not installed"
    echo
    echo "4. Available Space by Mount Point:"
    df -h --output=source,fstype,size,used,avail,pcent,target
    echo
    echo "5. Current LXD Storage Status:"
    lxc storage list
    echo
    echo "6. Available ZFS Pools (if using ZFS):"
    which zpool && zpool list 2>/dev/null || echo "ZFS not installed"
EOF
  # Add a delay between machines
  sleep 3
  echo "Comparing current info with previous info for machine: $machine"
  # Compare current info with previous info if it exists
  if [ -f "$previous_info_file" ]; then
    cp "$previous_info_file" "$backup_info_file"
    diff "$previous_info_file" "$current_info_file" > "$diff_file"
    if [ -s "$diff_file" ]; then
      echo "Changes detected for machine $machine on $timestamp. See $diff_file for details."
    else
      echo "No changes detected for machine $machine on $timestamp."
      rm "$diff_file"
    fi
  else
    echo "No previous info found for machine $machine. Saving current info."
  fi
  # Save current info as previous info for future comparisons
  cp "$current_info_file" "$previous_info_file"
done
echo "Information gathering complete. Check the $output_dir and $audit_dir directories for details."
