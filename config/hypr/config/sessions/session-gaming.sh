#!/bin/bash

# Launch Steam/Lutris if not running
pgrep steam >/dev/null || steam &
pgrep lutris >/dev/null || lutris &

# Move browser to AltWeb (workspace 5) if running
if hyprctl clients | grep "thorium-browser"; then
  hyprctl dispatch movetoworkspace 5,class:thorium-browser
fi

# Focus workspaces: Game (2) + Alt (5)
hyprctl dispatch workspace 2
hyprctl dispatch workspace 5