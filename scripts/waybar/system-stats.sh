#!/bin/bash

# Get CPU data from gopsuinfo
data=$(gopsuinfo -c gat)

# Extract CPU components
cpu_graph=$(echo "$data" | awk '{print $1}')
cpu_usage=$(echo "$data" | awk '{print $2}' | tr -d '')
cpu_temp=$(echo "$data" | awk '{print $3}' | tr -d '')

# Get RAM information
ram_percent=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
ram_used=$(free -m | awk '/Mem:/ {printf "%.1f", $3/1024}')
ram_total=$(free -m | awk '/Mem:/ {printf "%.1f", $2/1024}')

# Format output with Nerd Font icons
echo "{\"text\":\" $cpu_graph $cpu_usage  ${cpu_temp}  ${ram_used}GB/${ram_total}GB\"}"