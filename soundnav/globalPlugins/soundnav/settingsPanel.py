# -*- coding: utf-8 -*-
# settingsPanel.py - Configuration GUI panel
# Part of SoundNav add-on for NVDA

import config
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel
import wx
import addonHandler

addonHandler.initTranslation()

# Configuration key for this add-on
SOUNDNAV_CONFIG_KEY = "soundnav"

def init_configuration():
    """
    Initialize configuration specification.

    Defines the configuration structure and default values for the add-on.
    Must be called once during add-on initialization.
    """
    confspec = {
        "enabled": "boolean(default=True)",
        "suppressRoleLabels": "boolean(default=True)",
        "browseModeSound": "boolean(default=True)",
    }
    config.conf.spec[SOUNDNAV_CONFIG_KEY] = confspec

def get_config(key):
    """
    Get a configuration value.

    Args:
        key: Configuration key to retrieve

    Returns:
        The configuration value
    """
    return config.conf[SOUNDNAV_CONFIG_KEY][key]

def set_config(key, value):
    """
    Set a configuration value.

    Args:
        key: Configuration key to set
        value: Value to set
    """
    config.conf[SOUNDNAV_CONFIG_KEY][key] = value

class SoundNavSettingsPanel(SettingsPanel):
    """
    Settings panel for SoundNav add-on.

    Appears in NVDA's settings dialog under the "Sound Navigation" category.
    """

    # Translators: Title of the settings panel
    title = _("Sound Navigation")

    def makeSettings(self, settingsSizer):
        """
        Create the settings controls.

        Args:
            settingsSizer: The sizer to add controls to
        """
        sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

        # Checkbox to enable/disable the add-on
        # Translators: Label for checkbox to enable/disable Sound Navigation
        self.enabledCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=_("&Enable Sound Navigation"))
        )
        self.enabledCheckbox.SetValue(get_config("enabled"))

        # Checkbox to suppress spoken role labels
        # Translators: Label for checkbox to suppress role labels
        self.suppressRoleLabelsCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=_("&Suppress spoken role labels (e.g., 'button', 'link')"))
        )
        self.suppressRoleLabelsCheckbox.SetValue(get_config("suppressRoleLabels"))

        # Translators: Tooltip for suppress role labels checkbox
        self.suppressRoleLabelsCheckbox.SetToolTip(wx.ToolTip(
            _("When enabled, NVDA will not speak role labels like 'button' or 'link', "
              "playing only the sound. When disabled, both sounds and role labels will be spoken.")
        ))

        # Checkbox to enable browse mode sounds
        # Translators: Label for checkbox to enable browse mode sounds
        self.browseModeSoundCheckbox = sHelper.addItem(
            wx.CheckBox(self, label=_("&Play sounds during browse mode navigation (arrow keys)"))
        )
        self.browseModeSoundCheckbox.SetValue(get_config("browseModeSound"))

        # Translators: Tooltip for browse mode sound checkbox
        self.browseModeSoundCheckbox.SetToolTip(wx.ToolTip(
            _("When enabled, 3D sounds will play when navigating web pages with arrow keys "
              "and quick navigation keys (H, K, B, etc.) in browse mode.")
        ))

    def onSave(self):
        """
        Save configuration when user clicks OK or Apply.
        """
        set_config("enabled", self.enabledCheckbox.GetValue())
        set_config("suppressRoleLabels", self.suppressRoleLabelsCheckbox.GetValue())
        set_config("browseModeSound", self.browseModeSoundCheckbox.GetValue())
