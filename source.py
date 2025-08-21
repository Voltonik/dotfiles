import os
import sys
from pathlib import Path
import decman
import decman.config
import json

# Add the modules directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src" / "modules"))

from src.cachyos_packages import default_packages
from src.paru_wrapper import ParuWrapperCommands
from src.desktop import Desktop
from src.themer import Themer
from src.user import User


if os.environ.get("DBUS_SESSION_BUS_ADDRESS", "") == "":
    raise EnvironmentError("Environment variables not set. Make sure to run with sudo -E") 

repo_root = Path.cwd()
user_config = json.loads((repo_root / "data" / "user.json").read_text(encoding="utf-8"))

current_user = user_config["user"]

decman.config.debug_output = False
decman.config.suppress_command_output = False
decman.config.quiet_output = False
decman.config.enable_fpm = False
decman.config.commands = ParuWrapperCommands(current_user)

decman.modules += [
    Desktop(current_user),
    Themer(current_user),
    
    User(current_user),
]

decman.ignored_packages += default_packages
decman.packages += [
#AUR Packages:
    "decman"
]