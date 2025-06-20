#!/bin/bash

# Load environment variables
source "$(dirname "$0")/.env"

# Read machine IPs from environment variable
IFS=' ' read -r -a machines <<< "$MACHINE_IPS"
user="$DB_USER"

# Output directory
output_dir="$HOME/machine_info_audit"
mkdir -p "$output_dir"
output_file="$output_dir/lxd_version_report_$(date +'%Y-%m-%d_%H-%M-%S').txt"

# Temporary file to store results
temp_file="$(mktemp)"

# Header for output
printf "%-15s %-10s %-10s\n" "IP Address" "LXC" "LXD" > "$temp_file"
echo "--------------------------------------" >> "$temp_file"

# Loop through each machine and gather version info
for machine in "${machines[@]}"; do
    echo "Checking versions on $machine..."
    ssh -o StrictHostKeyChecking=no "$user@$machine" "lxc --version; lxd --version" > "$output_dir/$machine-versions.txt" 2>/dev/null
    
    # Extract LXC and LXD versions
    lxc_version=$(sed -n '1p' "$output_dir/$machine-versions.txt")
    lxd_version=$(sed -n '2p' "$output_dir/$machine-versions.txt")
    
    # Save to temporary file
    printf "%-15s %-10s %-10s\n" "$machine" "$lxc_version" "$lxd_version" >> "$temp_file"
done

echo "--------------------------------------" >> "$temp_file"

# Identify version mismatches
lxc_versions=($(awk 'NR>2 {print $2}' "$temp_file" | sort -u))
lxd_versions=($(awk 'NR>2 {print $3}' "$temp_file" | sort -u))

highlight_mismatch() {
    while read -r line; do
        if [[ "$line" =~ ${lxc_versions[0]} ]] && [[ "$line" =~ ${lxd_versions[0]} ]]; then
            echo "$line"
        else
            echo -e "\e[31m$line\e[0m" # Highlight in red
        fi
    done
}

# Print results with mismatches highlighted
highlight_mismatch < "$temp_file" | tee "$output_file"

# Clean up
rm "$temp_file"

echo "LXD version check complete. Results saved to: $output_file"

