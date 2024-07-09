# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import json
import os

from utils import resource_path

# APP SETTINGS
# ///////////////////////////////////////////////////////////////
class Settings(object):
    json_file = "settings.json"
    settings_path = resource_path(json_file)

    if not os.path.isfile(settings_path):
        print(f"WARNING: \"settings.json\" not found! Check in the folder {settings_path}")
    else:
        print(f"Settings file found: {settings_path}")
    
    # INIT SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Settings, self).__init__()

        # DICTIONARY WITH SETTINGS
        # Just to have objects references
        self.items = {}

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        # READ JSON FILE
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings

    def save_settings(self):
        # Implement your logic to update specific settings before saving
        # For example, updating the theme_name
        self.items["theme_name"] = "dark" if self.items["theme_name"] == "light" else "light"

        # Add any other settings you want to update before saving

        # Serialize and save the updated settings
        self.serialize()