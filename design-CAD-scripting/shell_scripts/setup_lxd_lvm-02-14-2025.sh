#!/bin/bash

# Source environment variables
source "$(dirname "$0")/.env"

# SSH Options Configuration
SSH_OPTS="-o StrictHostKeyChecking=no -t"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"

# Environment variables
user="$DB_USER"
info_host="$INFO_HOST"  # Added to .env
info_dir="$HOME/documents/scripts/machine_info_audit"
log_file="$HOME/documents/scripts/setup_lxd_lvm_$(date +'%Y-%m-%d_%H-%M-%S').log"

# Function to get machine configuration from .env
get_machine_config() {
    local machine=$1
    local var_name="MACHINE_CONFIG_${machine//./_}"
    local config="${!var_name}"
    
    if [ -z "$config" ]; then
        config="$DEFAULT_CONFIG"
    fi
    
    echo "$config"
}

# Main setup loop
for machine in "${machines[@]}"; do
    echo "Setting up LXD LVM on $machine..."
    
    # Get machine-specific configuration
    read device size setup_type <<< $(get_machine_config "$machine")
    
    # Fallback configuration handling
    if [ "$device" = "default_device" ] || [ -z "$device" ]; then
        latest_info_dir=$(ls -td $info_dir/*/ | head -n 1)
        info_file="$latest_info_dir/$machine-info.txt"
        ssh ${SSH_OPTS} "$user@$info_host" "cat $info_file" > /tmp/$machine-info.txt
        
        if [ -f "/tmp/$machine-info.txt" ]; then
            device=$(grep -Eo '/dev/sd[a-z]+' "/tmp/$machine-info.txt" | head -n 1)
            size="100G"
            setup_type="standard"
        else
            echo "Error: Info file for $machine not found and no configuration in .env."
            continue
        fi
    fi
    
    # Log start of setup
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting setup on $machine" >> "$log_file"
    
    # Execute remote commands
    ssh ${SSH_OPTS} "$user@$machine" << EOF
        # Get machine details
        hostname=\$(hostname)
        ip_address=\$(ip a | grep -i "inet ${INTERNAL_NET_PREFIX}." | awk '{print \$2}' | cut -d/ -f1)
        
        # Log machine information
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Machine: \$hostname (\$ip_address)" >> "$log_file"
        
        # System updates and LVM installation
        echo "Installing LVM tools..."
        sudo apt-get update
        sudo apt-get install -y lvm2
        
        # LVM setup based on configuration type
        if [ "$setup_type" = "lvm" ]; then
            echo "Creating logical volume..."
            sudo lvcreate -L $size -n lxd-lv ubuntu--vg
            lxc storage create lxd-storage lvm source=ubuntu--vg/lxd-lv
        else
            echo "Creating physical volume..."
            sudo pvcreate $device
            sudo vgcreate lxd-vg $device
            lxc storage create lxd-storage lvm source=lxd-vg
        fi
        
        # Create test container
        echo "Launching test container..."
        lxc launch ubuntu:20.04 my-container -s lxd-storage
EOF

    # Add delay between machines
    sleep 3
    echo "LXD LVM setup completed on $machine"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Setup completed on $machine" >> "$log_file"
done

echo "Setup complete. Check the log file at $log_file for details."
