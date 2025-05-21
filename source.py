import decman
import decman.config

from cachyos_packages import default_packages
from paru_wrapper import ParuWrapperCommands
from desktop import Desktop
from themer import Themer


current_user = "mark"

decman.config.debug_output = False
decman.config.suppress_command_output = False
decman.config.quiet_output = False
decman.config.enable_fpm = False
decman.config.commands = ParuWrapperCommands(current_user)

decman.modules += [
    Desktop(current_user),
    Themer(current_user)
]

decman.ignored_packages += default_packages
decman.packages += [
    "git",
    "neovim",

#AUR Packages:
    "decman",
    "thorium-browser-bin",
    "visual-studio-code-bin"
]

decman.enabled_systemd_units += [
    "NetworkManager.service",
    "bluetooth.service",
    "ly.service"
]