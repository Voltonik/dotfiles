from decman import Module, Directory, File, prg
from pathlib import Path
import json
import re
import shutil
import sys

class Desktop(Module):
    def __init__(self, current_user: str):
        self.current_user = current_user
        self.home_dir = f"/home/{current_user}"
        self.config_dest_dir = f"{self.home_dir}/.config"
        
        super().__init__(name="desktop", enabled=True, version="1")
        
        # write to source repo files (assumes repo root == cwd)
        repo_root = Path.cwd()
        try:
            # insert waybar icons inline in repo source waybar config
            self._insert_waybar_icons_inline(repo_root)
            # generate hyprland monitor/workspace snippet in repo source hypr config
            self._generate_hypr_snippet(repo_root)
        except Exception as e:
            print(f"[Desktop] Warning: post-init generation failed: {e}", file=sys.stderr)


    def pacman_packages(self) -> list[str]:
        return [
            "git",
            "neovim",
            "hyprland", "xorg-xwayland", "hyprland-protocols", "hyprlang", "hyprutils", "hyprwayland-scanner", "xdg-desktop-portal-hyprland", "xdg-desktop-portal",
            "ly",
            "polkit-gnome",
            "rofi-wayland", "rofi-calc",
            "waybar", "gopsuinfo",
            "network-manager-applet",
            "blueman",
            "bluez-utils",
            "nautilus",
            "swaybg",
            "swaylock",
            "swaync",
            "ntfs-3g",
            "btop",
            "mpd",
            "mpv",
            "wl-clipboard",
            "wl-clip-persist",
            "clipse",
            "slurp",
            "grim",
            "swappy",
            "kitty",
            "freetype2",
            "fontconfig",
            "cairo",
            "ttf-jetbrains-mono-nerd",
            "rsync",
            "ripgrep",
            "openssh",
            "python-packaging",

# AUR Packages:
            "thorium-browser-bin",
            "httpdirfs-git",
            "ttf-ms-win11-auto",
            "qt5ct",
            "qt6ct",
        ]
    
    def files(self) -> dict[str, File]:
        return {
            f"{self.config_dest_dir}/gtk-3.0/settings.ini": File(source_file="./config/theming/gtk-3.0/settings.ini", owner=self.current_user),
            f"{self.config_dest_dir}/gtk-4.0/settings.ini": File(source_file="./config/theming/gtk-4.0/settings.ini", owner=self.current_user),
            f"{self.home_dir}/.local/share/nautilus/scripts/images/change-wallpaper.sh": File(source_file="./scripts/system/change-wallpaper.sh", owner=self.current_user, permissions=0o755),
        }

    def directories(self) -> dict[str, Directory]:
        return {
            f"{self.config_dest_dir}/hypr/": Directory(
                source_directory="./config/desktop/hypr",
                owner=self.current_user,
                permissions=0o755
            ),
            f"{self.config_dest_dir}/waybar/": Directory(
                source_directory="./config/desktop/waybar",
                owner=self.current_user,
                permissions=0o755
            ),
            f"{self.config_dest_dir}/waybar/scripts": Directory(
                source_directory="./scripts/waybar",
                owner=self.current_user,
                permissions=0o755
            ),
            f"{self.config_dest_dir}/rofi/": Directory(
                source_directory="./config/desktop/rofi",
                owner=self.current_user,
                permissions=0o755
            ),
            f"{self.config_dest_dir}/swaync/": Directory(
                source_directory="./config/notifications/swaync",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/swaylock/": Directory(
                source_directory="./config/theming/swaylock",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/fish/": Directory(
                source_directory="./config/terminal/fish",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/kitty/": Directory(
                source_directory="./config/terminal/kitty",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/fontconfig/": Directory(
                source_directory="./config/fonts/fontconfig",
                owner=self.current_user,
            ),
            f"{self.config_dest_dir}/qt5ct/": Directory(
                source_directory="./config/theming/qt5ct",
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
        
    # ----------------------------
    # Waybar insertion helper(s)
    # ----------------------------
    def _insert_waybar_icons_inline(self, repo_root: Path):
        """Insert/update hyprland/workspaces block inside source repo waybar config (in-place)."""
        monitors_json = repo_root / "data" / "workspaces.json"
        waybar_cfg = repo_root / "config" / "desktop" / "waybar" / "config.jsonc"
        backup = waybar_cfg.with_suffix(".jsonc.bak")

        if not monitors_json.exists():
            raise FileNotFoundError(f"{monitors_json} not found (source monitors.json).")
        if not waybar_cfg.exists():
            raise FileNotFoundError(f"{waybar_cfg} not found (source waybar config).")

        try:
            cfg = json.loads(monitors_json.read_text(encoding="utf-8"))
        except Exception as e:
            raise RuntimeError(f"Failed to parse {monitors_json}: {e}")

        workspaces = cfg.get("workspaces", [])
        icons_map = {}
        persistent_map = {}

        for ws in workspaces:
            ws_id = ws.get("id")
            if ws_id is None:
                continue
            name = ws.get("name", "").strip()
            icon = ws.get("icon", "").strip()
            icons_map[str(ws_id)] = f"{icon}".strip()  # change to icon-only if needed
            persistent = ws.get("persistent", [])
            if not isinstance(persistent, list):
                persistent = []
            persistent_map[str(ws_id)] = persistent

        # Try JSON update first
        if self._safe_json_update(waybar_cfg, icons_map, persistent_map, backup):
            return
        # Fallback to regex
        if self._regex_patch(waybar_cfg, icons_map, persistent_map, backup):
            return
        raise RuntimeError("Failed to patch waybar config by either JSON or regex methods.")

    def _safe_json_update(self, path: Path, icons_map: dict, persistent_map: dict, backup: Path) -> bool:
        try:
            text = path.read_text(encoding="utf-8")
            cfg = json.loads(text)
        except Exception:
            return False

        if "hyprland/workspaces" not in cfg:
            cfg["hyprland/workspaces"] = {}

        module = cfg["hyprland/workspaces"]
        module["format"] = module.get("format", "{icon}")
        module["format-icons"] = icons_map
        module["persistent-workspaces"] = persistent_map
        module["on-scroll-up"] = module.get("on-scroll-up", "hyprctl dispatch workspace -1")
        module["on-scroll-down"] = module.get("on-scroll-down", "hyprctl dispatch workspace +1")

        shutil.copy2(path, backup)
        path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return True

    def _regex_patch(self, path: Path, icons_map: dict, persistent_map: dict, backup: Path) -> bool:
        text = path.read_text(encoding="utf-8")

        m = re.search(r'("hyprland/workspaces"\s*:\s*)\{', text)
        if not m:
            return False

        open_pos = text.find("{", m.end(1)-1)
        if open_pos == -1:
            return False

        i = open_pos
        depth = 0
        end_pos = None
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end_pos = i
                    break
            i += 1
        if end_pos is None:
            return False

        new_block = {
            "format": "{icon}",
            "format-icons": icons_map,
            "persistent-workspaces": persistent_map,
            "on-scroll-up": "hyprctl dispatch workspace -1",
            "on-scroll-down": "hyprctl dispatch workspace +1"
        }
        new_block_text = json.dumps(new_block, indent=4, ensure_ascii=False)

        new_text = text[:open_pos] + new_block_text + text[end_pos+1:]
        shutil.copy2(path, backup)
        path.write_text(new_text, encoding="utf-8")
        return True

    # ----------------------------
    # Hyprland generator
    # ----------------------------
    def _generate_hypr_snippet(self, repo_root: Path):
        """
        Generate a hyprland monitors/workspaces snippet from repo's config/hypr/monitors.json
        and write it to repo's config/hypr/config/monitor.conf (backup created).
        """
        monitors_json = repo_root / "data" / "workspaces.json"
        hypr_out = repo_root / "config" / "desktop" / "hypr" / "config" / "monitor.conf"
        backup = hypr_out.with_suffix(".conf.bak")

        if not monitors_json.exists():
            raise FileNotFoundError(f"{monitors_json} not found (source monitors.json).")
        # ensure output directory exists
        hypr_out.parent.mkdir(parents=True, exist_ok=True)

        try:
            cfg = json.loads(monitors_json.read_text(encoding="utf-8"))
        except Exception as e:
            raise RuntimeError(f"Failed to parse {monitors_json}: {e}")

        monitors = cfg.get("monitors", {})
        workspaces = cfg.get("workspaces", [])

        hypr_lines = []
        hypr_lines.append("# generated by generate_hypr_snippet")
        hypr_lines.append("# monitor variables")
        # create $<key> = <dev> lines
        for mkey, dev in monitors.items():
            var = mkey.strip()
            hypr_lines.append(f"${var} = {dev}, preferred, auto, 1")
        hypr_lines.append("")

        # register monitors
        for mkey in monitors.keys():
            var = mkey.strip()
            hypr_lines.append(f"monitor = ${var}")
        hypr_lines.append("")

        # helper: fallback monitor if workspace references missing one
        first_monitor_key = next(iter(monitors.keys()), None)

        # workspaces
        hypr_lines.append("# workspaces")
        for ws in workspaces:
            ws_id = ws.get("id")
            if ws_id is None:
                continue
            name = ws.get("name", f"WS{ws_id}")
            layout = ws.get("layout", "master")
            monitor_ref = ws.get("monitor")
            # determine monitor expression
            if monitor_ref and monitor_ref in monitors:
                monitor_expr = f"monitor:${monitor_ref}"
            elif first_monitor_key is not None:
                monitor_expr = f"monitor:${first_monitor_key}"
            else:
                monitor_expr = ""  # no monitor info

            # quote name if it contains spaces/commas/colons
            if any(c.isspace() for c in name) or ("," in name) or (":" in name):
                name_field = f'name:"{name}"'
            else:
                name_field = f"name:{name}"

            parts = [f"workspace = {ws_id}", name_field]
            if monitor_expr:
                parts.append(monitor_expr)
            parts.append(f"layout:{layout}")
            hypr_lines.append(", ".join(parts))

        hypr_lines.append("")
        # auto-assignments (from JSON instead of hardcoded)
        auto = cfg.get("autoassign", {})
        if auto:
            hypr_lines.append("# Auto-assignment")

            # window rules
            for ws_id, rules in auto.get("windowrules", {}).items():
                for rule in rules:
                    hypr_lines.append(f"windowrulev2 = workspace {ws_id}, {rule}")
            hypr_lines.append("")

        # binds
        binds = cfg.get("binds", {})
        if binds:
            for bind in binds:
                hypr_lines.append(bind)

        # write backup and new file
        if hypr_out.exists():
            shutil.copy2(hypr_out, backup)
        hypr_out.write_text("\n".join(hypr_lines) + "\n", encoding="utf-8")

        print(f"[Desktop] Wrote hypr snippet to {hypr_out} (backup at {backup} if existed).")
