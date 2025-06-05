#!/bin/bash

if [[ -z "$1" ]]; then
    echo "󱖦"
else
    killall -q rofi
    rofi -show calc -modi calc -no-show-match -no-sort -calc-command "echo -n '{result}' | wl-copy"
fi