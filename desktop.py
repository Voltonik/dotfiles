from decman import Module, Directory, File, prg

class Desktop(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"{self.home_dir}/.config"
        
        super().__init__(name="desktop", enabled=True, version="1")

    def pacman_packages(self) -> list[str]:
        return [
            "git",
            "neovim",
            "hyprland", "hyprland-protocols", "hyprlang", "hyprutils", "hyprwayland-scanner", "xdg-desktop-portal-hyprland",
            "xdg-desktop-portal",
            "ly",
            "waybar",
            "gopsuinfo",
            "swaybg",
            "swaylock",
            "swayidle",
            "rofi-wayland",
            "rofi-calc",
            "swaync",
            "nautilus",
            "btop",
            "mpd",
            "polkit-gnome",
            "wl-clipboard",
            "wl-clip-persist",
            "clipse",
            "slurp",
            "grim",
            "swappy",
            "kitty",
            "network-manager-applet",
            "blueman",
            "bluez-utils",
            "freetype2",
            "fontconfig",
            "cairo",
            "ttf-jetbrains-mono-nerd",

# AUR Packages:
            "wlogout",
            "thorium-browser-bin",
            "httpdirfs-git",
            "ttf-ms-win11-auto",
            "qt5ct",
            "qt6ct",
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
                permissions=0o755
            ),
            f"{self.config_dest_dir}/rofi/": Directory(
                source_directory="./config/rofi",
                owner=self.current_user,
                permissions=0o755
            ),
            f"{self.config_dest_dir}/swaync/": Directory(
                source_directory="./config/swaync",
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
            f"{self.config_dest_dir}/kitty/": Directory(
                source_directory="./config/kitty",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/fontconfig/": Directory(
                source_directory="./config/fontconfig",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/qt5ct/": Directory(
                source_directory="./config/qt5ct",
                owner=self.current_user,
            ),
        }
    
    def systemd_units(self) -> list[str]:
        return [
            "NetworkManager.service",
            "bluetooth.service",
            "ly.service",
        ]

    def systemd_user_units(self) -> dict[str, list[str]]:
        return {
            self.current_user: []
        }

    def after_update(self):
        print("-------Reloading Desktop-------")
        prg(["hyprctl", "reload"], self.current_user)
        