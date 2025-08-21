#!/bin/sh
# Kill all existing Waybar processes
killall -q waybar

# Wait until processes are terminated
while pgrep -x waybar >/dev/null; do sleep 0.1; done

# Launch Waybar with explicit config
waybar -c ~/.config/waybar/config.jsonc &