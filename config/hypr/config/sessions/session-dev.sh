#!/bin/bash

# Launch Unity/Code if not running
pgrep Unity >/dev/null || unityhub &
pgrep code >/dev/null || code &

# Ensure Web is in workspace 1
if hyprctl clients | grep "thorium-browser"; then
  hyprctl dispatch movetoworkspace 1,class:thorium-browser
fi

# Focus workspaces: Web (1) + Code (4)
hyprctl dispatch workspace 1
hyprctl dispatch workspace 4