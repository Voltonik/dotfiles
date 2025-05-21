import os
import shutil
from decman import Module, File, Directory

class Themer(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"/home/{current_user}/.config"

        self._generate_theme_files()
        self._install_fonts()
        
        super().__init__(name="themer", enabled=True, version="1")

    def _generate_theme_files(self):
        wal_cache_dir = f"{self.home_dir}/.cache/wal"
        wal_waybar_colors_src = f"{self.home_dir}/.cache/wal/colors-waybar.css"

        os.system(f"sudo -u {self.current_user} wal --theme theme.json")

        os.makedirs("config/presets/user", exist_ok=True)
        os.makedirs("config/Kvantum/pywal", exist_ok=True)

        shutil.copyfile(f"{wal_cache_dir}/pywal.json", "config/presets/user/pywal.json")
        shutil.copyfile(f"{wal_cache_dir}/pywal.kvconfig", "config/Kvantum/pywal/pywal.kvconfig")
        shutil.copyfile(f"{wal_cache_dir}/pywal.svg", "config/Kvantum/pywal/pywal.svg")

        if os.path.exists(wal_waybar_colors_src) and os.path.exists("config/waybar"):
            shutil.copyfile(wal_waybar_colors_src, "config/waybar/colors-waybar.css")
        else:
            raise FileNotFoundError(f"Pywal Waybar colors file not found at {wal_waybar_colors_src}")

    def _install_fonts(self):
        font_dir = f"{self.home_dir}/.local/share/fonts/"
        os.makedirs(font_dir, exist_ok=True)
        for font in os.listdir("./custom-fonts"):
            src = f"./custom-fonts/{font}"
            dest = f"{font_dir}{font}"
            if os.path.isfile(src):
                shutil.copyfile(src, dest)
        
        os.system(f"fc-cache -f -v {font_dir}")

    def pacman_packages(self) -> list[str]:
        return [
            "python-pywal16",
            "python-yapsy-git",
            "gradience",
            "kvantum",
            "adw-gtk-theme",
            "httpdirfs-git",
            "ttf-ms-win11-auto"
        ]

    def files(self) -> dict[str, File]:
        return {
            f"{self.config_dest_dir}/presets/user/pywal.json": File(source_file="./config/presets/user/pywal.json", owner=self.current_user),
        }

    def directories(self) -> dict[str, Directory]:
        return {
            f"{self.config_dest_dir}/Kvantum/": Directory(source_directory="./config/Kvantum", owner=self.current_user),
            f"{self.config_dest_dir}/wal/": Directory(source_directory="./config/wal", owner=self.current_user),
        }

    def after_update(self):
        print("-------Applying gradience and kvantum themes-------")
        os.system(f"sudo --user {self.current_user} gradience-cli apply -n pywal --gtk both")
        os.system(f"sudo --user {self.current_user} kvantummanager --set pywal")