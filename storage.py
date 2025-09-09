import os
import sys
from pathlib import Path
import json
import shutil
from shutil import copyfile

class Storage:
    def __init__(self, app_name="ScreenSaverApp"):
        self.app_name = app_name
        self.base_dir = self.get_config_dir()
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.config_dir = self.base_dir / "config"
        self.background_dir = self.base_dir / "backgrounds"
        self.config_dir.mkdir(exist_ok=True)
        self.background_dir.mkdir(exist_ok=True)

    def get_config_dir(self):
        if sys.platform == "win32":
            base = Path(os.getenv("APPDATA"))
        elif sys.platform == "darwin": # macOS
            base = Path.home() / "Library" / "Application Support"
        else:  # Linux/Unix
            base = Path.home() / ".config"
        return base / self.app_name

    def resource_path(self, relative_path):
        if getattr(sys, "frozen", False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent
        return base_path / relative_path
    
    def copy_defaults(self, defaults_folder="defaults"):
        defaults_path = self.resource_path(defaults_folder)
        if not defaults_path.exists():
            defaults_path.mkdir(parents=True, exist_ok=True)

        # JSON
        for json_file in defaults_path.glob("*.json"):
            dest = self.config_dir / json_file.name
            if not dest.exists():
                shutil.copy(json_file, dest)
            else:
                self.update_settings()

        # images
        defaults_path = defaults_path / "backgrounds"
        for ext in ("*.png", "*.jpg"):
            for img_file in defaults_path.glob(ext):
                dest = self.background_dir / img_file.name
                if not dest.exists():
                    shutil.copy(img_file, dest)

    def save_json(self, filename, data):
        file_path = self.config_dir / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_json(self, filename, default=None):
        file_path = self.config_dir / filename
        if not file_path.exists():
            return default
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_settings(self, default_file="defaults/settings.json"):
        default_path = self.resource_path(default_file)
        if not default_path.exists():
            return
        config_path = self.config_dir / "settings.json"
        
        with open(default_path, "r", encoding="utf-8") as f:
            default_settings = json.load(f)

        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                current_settings = json.load(f)
        else:
            current_settings = {}

        for key, value in default_settings.items():
            if key not in current_settings:
                current_settings[key] = value

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(current_settings, f, indent=4)

    def save_file(self, filename, source_path):
        dest = self.background_dir / filename
        copyfile(source_path, dest)
        return dest

    def get_file_path(self, filename, folder="backgrounds"):
        if folder == "config":
            return self.config_dir / filename
        elif folder == "backgrounds":
            return self.background_dir / filename
        else:
            return self.base_dir / filename

    def list_files(self, folder="backgrounds"):
        if folder == "config":
            return list(self.config_dir.iterdir())
        elif folder == "backgrounds":
            return list(self.background_dir.iterdir())
        else:
            return list(self.base_dir.iterdir())

    def file_exists(self, filename, folder="backgrounds"):
        return self.get_file_path(filename, folder).exists()
