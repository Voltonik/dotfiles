import os
import decman
import decman.config

from cachyos_packages import default_packages
from paru_wrapper import ParuWrapperCommands
from desktop import Desktop
from themer import Themer
from mark import Mark


if os.environ.get("DBUS_SESSION_BUS_ADDRESS", "") == "":
    raise EnvironmentError("Environment variables not set. Make sure to run with sudo -E") 

current_user = "mark"

decman.config.debug_output = False
decman.config.suppress_command_output = False
decman.config.quiet_output = False
decman.config.enable_fpm = False
decman.config.commands = ParuWrapperCommands(current_user)

decman.modules += [
    Desktop(current_user),
    Themer(current_user),
    
    Mark(current_user),
]

decman.ignored_packages += default_packages
decman.packages += [
#AUR Packages:
    "decman",
    "visual-studio-code-bin"
]