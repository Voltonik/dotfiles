#!/usr/bin/env bash
set -euo pipefail

# Usage:
# session-spawn.sh "<exec-cmd>" "<app-class>" [left_ws] [right_ws]
# Example:
# session-spawn.sh "thorium-browser" "thorium-browser" 1 5

if [[ $# -lt 2 ]]; then
  cat >&2 <<EOF
Usage:
  $0 "<exec-cmd>" "<app-class>" [left_ws] [right_ws]

Examples:
  $0 "thorium-browser" "thorium-browser"
  $0 "firefox --new-window" "Firefox" 1 7

Notes:
  - Wrap the exec command in quotes if it contains args.
  - app-class must match the 'class' value shown by 'hyprctl clients'.
EOF
  exit 1
fi

EXEC_CMD="$1"         # full command to launch (may contain spaces/args)
APP_CLASS="$2"        # class name as hyprctl reports it (case sensitive)
LEFT_WS="${3:-1}"     # default left workspace id
RIGHT_WS="${4:-5}"    # default right workspace id

# Ensure jq & hyprctl are available
command -v hyprctl >/dev/null 2>&1 || { echo "hyprctl not found" >&2; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "jq not found" >&2; exit 1; }

# current workspace
CURRENT_WS=$(hyprctl activeworkspace -j | jq -r '.id')

# find windows of this class (addresses)
mapfile -t ADDRS < <(hyprctl clients -j | jq -r --arg cls "$APP_CLASS" '.[] | select(.class==$cls) | .address')

if [[ ${#ADDRS[@]} -gt 0 ]]; then
  # app already has at least one window; focus the first one found
  TARGET_ADDR="${ADDRS[0]}"
  TARGET_WS=$(hyprctl clients -j | jq -r --arg addr "$TARGET_ADDR" '.[] | select(.address==$addr) | .workspace.id')

  # only dispatch if not already on that workspace (prevents toggle behavior)
  if [[ "$CURRENT_WS" != "$TARGET_WS" ]]; then
    hyprctl dispatch workspace "$TARGET_WS"
  fi
  exit 0
fi

# app not running → decide where to spawn based on occupancy of workspaces
LEFT_COUNT=$(hyprctl clients -j | jq --argjson ws "$LEFT_WS" '[.[] | select(.workspace.id==$ws)] | length')
RIGHT_COUNT=$(hyprctl clients -j | jq --argjson ws "$RIGHT_WS" '[.[] | select(.workspace.id==$ws)] | length')

launch_and_focus() {
  local target_ws="$1"
  # Dispatch only if not already on that workspace
  if [[ "$CURRENT_WS" != "$target_ws" ]]; then
    hyprctl dispatch workspace "$target_ws"
  fi
  # launch detached so the script can exit immediately
  setsid bash -lc "$EXEC_CMD" >/dev/null 2>&1 &
}

if [[ "$LEFT_COUNT" -eq 0 ]]; then
  # Spawn on left
  launch_and_focus "$LEFT_WS"
elif [[ "$RIGHT_COUNT" -eq 0 ]]; then
  # Spawn on right
  launch_and_focus "$RIGHT_WS"
else
  # Both filled → fallback to left
  launch_and_focus "$LEFT_WS"
fi

exit 0