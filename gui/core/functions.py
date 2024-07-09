# ///////////////////////////////////////////////////////////////
#
# BY: 
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import os

from utils import resource_path

# APP FUNCTIONS
# ///////////////////////////////////////////////////////////////
class Functions:

    # SET SVG ICON
    # ///////////////////////////////////////////////////////////////
    def set_svg_icon(icon_name):
        folder = "gui/images/svg_icons/"
        icon = resource_path(os.path.join(folder, icon_name))
        return icon

    # SET SVG IMAGE
    # ///////////////////////////////////////////////////////////////
    def set_svg_image(icon_name):
        folder = "gui/images/svg_images/"
        icon = resource_path(os.path.join(folder, icon_name))
        return icon

    # SET IMAGE
    # ///////////////////////////////////////////////////////////////
    def set_image(image_name):
        folder = "gui/images/images/"
        image = resource_path(os.path.join(folder, image_name))
        return image