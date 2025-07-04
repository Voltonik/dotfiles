from decman import Module

class Mark(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"{self.home_dir}/.config"
        
        super().__init__(name="mark", enabled=True, version="1")

    def pacman_packages(self) -> list[str]:
        return [
            "discord",
            "dotnet-sdk",
            "zlib",
            "lib32-zlib",
            
# AUR Packages:
            "unityhub",
            "plasticscm-client-core",
            "plasticscm-client-gui",
            "umu-launcher",
            "lutris",
        ]
        