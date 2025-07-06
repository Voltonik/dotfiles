import os
import shutil
from decman import Module, File, Directory, prg
import configparser

class Themer(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"/home/{current_user}/.config"
        
        super().__init__(name="themer", enabled=True, version="1")

    def _generate_theme_files(self):
        wal_cache_dir = f"{self.home_dir}/.cache/wal"

        prg(["wal", "--theme", "theme.json"], self.current_user)

        os.makedirs(f"{self.config_dest_dir}/presets/user", exist_ok=True)
        os.makedirs(f"{self.config_dest_dir}/Kvantum/pywal", exist_ok=True)
        
        shutil.copyfile(f"{wal_cache_dir}/pywal.json", f"{self.config_dest_dir}/presets/user/pywal.json")
        shutil.copyfile(f"{wal_cache_dir}/pywal.kvconfig", f"{self.config_dest_dir}/Kvantum/pywal/pywal.kvconfig")
        shutil.copyfile(f"{wal_cache_dir}/pywal.svg", f"{self.config_dest_dir}/Kvantum/pywal/pywal.svg")
        
        wal_colors_css_src = f"{self.home_dir}/.cache/wal/colors-css.css"

        if os.path.exists(wal_colors_css_src):
            for css_dir in ["waybar", "swaync"]:
                if os.path.exists(f"{self.config_dest_dir}/{css_dir}"):
                    shutil.copyfile(wal_colors_css_src, f"{self.config_dest_dir}/{css_dir}/pywal-colors.css")

    def _install_fonts(self):
        font_dir = f"{self.home_dir}/.local/share/fonts/"
        os.makedirs(font_dir, exist_ok=True)
        for font in os.listdir("./custom-fonts"):
            src = f"./custom-fonts/{font}"
            dest = f"{font_dir}{font}"
            if os.path.isfile(src):
                shutil.copyfile(src, dest)
        
        os.system(f"fc-cache -f")
        
    def _set_gsettings(self):
        gtk3_config = f"{self.config_dest_dir}/gtk-3.0/settings.ini"
        config = configparser.ConfigParser()
        config.read(gtk3_config)
        if "Settings" not in config:
            print(f"No [Settings] section in {gtk3_config}.. Not applying gsettings")
            return;
        settings = config["Settings"]
        gnome_schema = "org.gnome.desktop.interface"
        settings_map = {
            "gtk-theme": "gtk-theme-name",
            "icon-theme": "gtk-icon-theme-name",
            "cursor-theme": "gtk-cursor-theme-name",
            "font-name": "gtk-font-name",
        }
        
        for g_key, ini_key in settings_map.items():
            if ini_key in settings:
                value = settings.get(ini_key)
                print(f"Setting {gnome_schema} {g_key} to '{value}'")
                prg(["gsettings", "set", gnome_schema, g_key, value], self.current_user)
                
        if settings.getboolean("gtk-application-prefer-dark-theme", fallback=None) is not None:
            prefer_dark = settings.getboolean("gtk-application-prefer-dark-theme")
            color_value = 'prefer-dark' if prefer_dark else 'default'
            print(f"Set {gnome_schema} color-scheme to '{color_value}'")
            prg(["gsettings", "set", gnome_schema, "color-scheme", color_value], self.current_user)

    def pacman_packages(self) -> list[str]:
        return [
            "python-pywal16",
            "python-yapsy-git",
            "gradience",
            "kvantum",
            "adw-gtk-theme",
            "ttf-roboto"
        ]

    def files(self) -> dict[str, File]:
        return {
            f"{self.config_dest_dir}/Kvantum/kvantum.kvconfig": File(source_file="./config/Kvantum/kvantum.kvconfig", owner=self.current_user),
        }

    def directories(self) -> dict[str, Directory]:
        return {
            f"{self.config_dest_dir}/wal/": Directory(source_directory="./config/wal", owner=self.current_user),
        }

    def after_update(self):
        print("-------Applying gradience and kvantum themes-------")
        
        cached_theme_json = f"{self.home_dir}/.cache/wal/colors.json"
        if os.path.exists(cached_theme_json):
            import json

            with open(cached_theme_json, 'r') as f:
                cached_theme = json.loads(f.read())
            with open("theme.json", 'r') as f:
                current_theme = json.loads(f.read())
            
            if all(cached_theme.get(key) == current_theme.get(key) for key in current_theme):
                print("Current theme is the same as cached theme, skipping applying the theme")
                return
        
        self._generate_theme_files()
        self._install_fonts()
        self._set_gsettings()
        
        prg(["gradience-cli", "apply", "-n", "pywal", "--gtk", "both"], self.current_user)
        prg(["kvantummanager", "--set", "pywal"], self.current_user)