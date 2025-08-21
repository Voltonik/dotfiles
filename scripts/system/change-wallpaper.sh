#!/usr/bin/env bash

#!/usr/bin/env bash

# Nautilus passes selected file paths via this variable:
# We’ll take only the first one.
read -r WALLPAPER_PATH _ <<< "$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"

# Path to your theme.json in your dotfiles repo
THEME_JSON="$HOME/dotfiles/theme.json"

# Sanity check: file exists and is a regular file
if [[ ! -f "$WALLPAPER_PATH" ]]; then
    zenity --error --text="No valid file selected!"
    exit 1
fi

# Sanity check: theme.json exists
if [[ ! -f "$THEME_JSON" ]]; then
    zenity --error --text="Cannot find theme file at $THEME_JSON"
    exit 1
fi

# Use jq to update the "wallpaper" key in theme.json
# Requires: sudo apt install jq   (or your distro’s equivalent)
tmpfile=$(mktemp)
jq --arg wp "$WALLPAPER_PATH" '.wallpaper = $wp' "$THEME_JSON" > "$tmpfile" \
    && mv "$tmpfile" "$THEME_JSON" \
    || { zenity --error --text="Failed to update $THEME_JSON"; exit 1; }

# Now apply the updated theme
wal --theme "$THEME_JSON"
