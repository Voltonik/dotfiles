from decman import Module, Directory, File

class Desktop(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"{self.home_dir}/.config"
        

        super().__init__(name="desktop", enabled=True, version="1")

    def pacman_packages(self) -> list[str]:
        return [
            "hyprland",
            "swaybg",
            "swaylock",
            "swayidle",
            "ly",
            "waybar",
            "wofi",
            "btop",
            "mako",
            "nautilus",
            "xdg-desktop-portal",
            "xdg-desktop-portal-hyprland",
            "wl-clipboard",
            "slurp",
            "grim",
            "swappy",
            "kitty",
            "network-manager-applet",

# AUR Packages:
            "wlogout",
        ]
    
    def files(self) -> dict[str, File]:
        return {
            f"{self.config_dest_dir}/gtk-3.0/settings.ini": File(source_file="./config/gtk-3.0/settings.ini", owner=self.current_user),
            f"{self.config_dest_dir}/gtk-4.0/settings.ini": File(source_file="./config/gtk-4.0/settings.ini", owner=self.current_user),
        }

    def directories(self) -> dict[str, Directory]:
        return {
            f"{self.config_dest_dir}/hypr/": Directory(
                source_directory="./config/hypr",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/waybar/": Directory(
                source_directory="./config/waybar",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/wofi/": Directory(
                source_directory="./config/wofi",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/mako/": Directory(
                source_directory="./config/mako",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/wlogout/": Directory(
                source_directory="./config/wlogout",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/swaylock/": Directory(
                source_directory="./config/swaylock",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/qt5ct/": Directory(
                source_directory="./config/qt5ct",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/fish/": Directory(
                source_directory="./config/fish",
                owner=self.current_user,
            ),
        }

    def systemd_user_units(self) -> dict[str, list[str]]:
        return {
            self.current_user: []
        }

    def after_update(self):
        print("-------Reloading Desktop-------")