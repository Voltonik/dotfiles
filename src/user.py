from decman import Module

class User(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"{self.home_dir}/.config"
        
        super().__init__(name=f"user ({current_user})", enabled=True, version="1")

    def pacman_packages(self) -> list[str]:
        return [
            "discord",
            "dotnet-sdk",
            "zlib",
            "lib32-zlib",
            "aspnet-runtime",
            "audacity",
            "obs-studio",
            "docker", "docker-desktop",
            "github-cli",
            "nodejs", "npm",
            "qbittorrent",
            
# AUR Packages:
            "vesktop",
            "visual-studio-code-bin",
            "unityhub",
            "plasticscm-client-core",
            "plasticscm-client-gui",
            "umu-launcher",
            "lutris",
        ]
        